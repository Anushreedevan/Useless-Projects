# File: app.py (Final, clean version using playsound)

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
whistle_count_threshold = 3  # The number of whistles to listen for
whistle_time_interval = 2.0  # Time in seconds between successive whistles
last_whistle_time = 0.0
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
# Adjust these values as needed for best detection
WHISTLE_FREQUENCY = 4000
FREQUENCY_TOLERANCE = 500
WHISTLE_THRESHOLD = 5000000

def listen_for_whistles():
    """
    This function will run in a separate thread to detect whistles
    and update the global whistle count.
    """
    global whistle_count, is_listening, last_whistle_time

    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK,
                    exception_on_overflow=False)

    print("Audio stream started. Listening for whistles...")

    while is_listening:
        data = stream.read(CHUNK, exception_on_overflow=False)
        audio_data = np.frombuffer(data, dtype=np.int16)

        # --- Whistle Detection Logic ---
        yf = rfft(audio_data)
        xf = rfftfreq(CHUNK, 1 / RATE)
        peak_frequency = xf[np.argmax(np.abs(yf))]
        peak_intensity = np.abs(yf[np.argmax(np.abs(yf))])

        if abs(peak_frequency - WHISTLE_FREQUENCY) < FREQUENCY_TOLERANCE and peak_intensity > WHISTLE_THRESHOLD:
            current_time = time.time()
            # Check if this is the first whistle or if enough time has passed since the last whistle
            if whistle_count == 0 or (current_time - last_whistle_time) >= whistle_time_interval:
                whistle_count += 1
                last_whistle_time = current_time
                print(f"Whistle detected! Count: {whistle_count}")
            
            # --- Amma's voice logic ---
            if whistle_count >= whistle_count_threshold:
                play_amma_sound()
                whistle_count = 0 # Reset the counter
                last_whistle_time = 0.0 # Reset timer

    # --- Clean up after listening stops ---
    stream.stop_stream()
    stream.close()
    p.terminate()
    whistle_count = 0 # Reset count when stopped
    last_whistle_time = 0.0

@app.route('/start_listening')
def start_listening():
    global is_listening, audio_thread, whistle_count, last_whistle_time
    if not is_listening:
        is_listening = True
        whistle_count = 0 # Reset count at the start
        last_whistle_time = 0.0 # Reset timer at the start
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

