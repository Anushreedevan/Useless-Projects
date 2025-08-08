# File: app.py (Final, clean version for Hackathon)

# All imports should be at the top of the file
import os
import threading
import pyaudio
import numpy as np
import time
from flask import Flask, jsonify
from scipy.fft import rfft, rfftfreq
from playsound import playsound

# --- 1. Set up the Flask application ---
app = Flask(__name__)

# --- 2. Shared variables for the application state ---
whistle_count = 0
whistle_count_threshold = 3  # Total number of whistles to count
first_whistle_time = None
is_listening = False
audio_thread = None

# --- New function to play the sound using playsound ---
def play_amma_sound():
    """Plays the Amma sound file using the playsound library."""
    try:
        playsound("amma_off_cooker.wav")
        print("Amma's voice played successfully!")
    except Exception as e:
        print(f"Error playing sound: {e}")

# --- 3. Audio stream parameters (Same as your old scripts) ---
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100

# --- 4. Whistle detection parameters ---
# These are for the initial whistle detection.
# You can adjust these values to make the detection more adaptable to different whistles.
# WHISTLE_FREQUENCY: The main frequency of a pressure cooker whistle (e.g., 4000 Hz).
# FREQUENCY_TOLERANCE: How far from the WHISTLE_FREQUENCY the sound can be to be counted.
# WHISTLE_THRESHOLD: The minimum volume/power of the sound to be considered a whistle.
WHISTLE_FREQUENCY = 4000
FREQUENCY_TOLERANCE = 500
WHISTLE_THRESHOLD = 5000000

def listen_for_whistles():
    """
    This function will run in a separate thread to detect the first whistle
    and then count subsequent whistles based on a timer.
    """
    global whistle_count, is_listening, first_whistle_time

    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK,
                    exception_on_overflow=False)

    print("Audio stream started. Waiting for the first whistle...")

    while is_listening:
        data = stream.read(CHUNK, exception_on_overflow=False)
        audio_data = np.frombuffer(data, dtype=np.int16)

        # --- Logic for the first whistle ---
        if first_whistle_time is None:
            yf = rfft(audio_data)
            xf = rfftfreq(CHUNK, 1 / RATE)
            peak_frequency = xf[np.argmax(np.abs(yf))]
            peak_intensity = np.abs(yf[np.argmax(np.abs(yf))])

            if abs(peak_frequency - WHISTLE_FREQUENCY) < FREQUENCY_TOLERANCE and peak_intensity > WHISTLE_THRESHOLD:
                whistle_count = 1
                first_whistle_time = time.time()
                print(f"First whistle detected! The timer has started.")
        
        # --- Logic for subsequent whistles (time-based) ---
        elif whistle_count < whistle_count_threshold:
            elapsed_time = time.time() - first_whistle_time
            # Increment the counter every 10 seconds
            new_whistle_count = int(elapsed_time / 10) + 1
            if new_whistle_count > whistle_count:
                whistle_count = new_whistle_count
                print(f"Time-based whistle counted! Current count: {whistle_count}")

        # --- Final check to play the sound ---
        if whistle_count >= whistle_count_threshold:
            print(f"Whistle count threshold reached: {whistle_count_threshold}")
            play_amma_sound()
            whistle_count = 0  # Reset the counter
            first_whistle_time = None # Reset the timer

    # --- Clean up after listening stops ---
    stream.stop_stream()
    stream.close()
    p.terminate()
    whistle_count = 0
    first_whistle_time = None


@app.route('/start_listening')
def start_listening():
    global is_listening, audio_thread, whistle_count, first_whistle_time
    if not is_listening:
        is_listening = True
        whistle_count = 0 # Reset count at the start
        first_whistle_time = None # Reset timer at the start
        audio_thread = threading.Thread(target=listen_for_whistles, daemon=True)
        audio_thread.start()
        return jsonify({"status": "Listening started"})
    return jsonify({"status": "Already listening"})

@app.route('/stop_listening')
def stop_listening():
    global is_listening
    if is_listening:
        is_listening = False
        return jsonify({"status": "Listening stopped"})
    return jsonify({"status": "Not currently listening"})

@app.route('/get_count')
def get_count():
    return jsonify({"count": whistle_count})

if __name__ == '__main__':
    app.run(debug=True)