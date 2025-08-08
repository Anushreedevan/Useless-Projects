# File: app.py (This is our final, integrated backend code)

from flask import Flask, jsonify
import threading
import pyaudio
import numpy as np
import os
# --- Add this line to tell pydub where to find FFmpeg ---
# Use the correct path to your FFmpeg bin folder
os.environ["PATH"] += os.pathsep + r"C:\Users\Aparna\Downloads\ffmpeg-7.1.1-essentials_build\ffmpeg-7.1.1-essentials_build\bin"

# The rest of your code follows
from flask import Flask, jsonify
import threading
# etc.
from scipy.fft import rfft, rfftfreq
from pydub import AudioSegment
from pydub.playback import play

# --- 1. Set up the Flask application ---
app = Flask(__name__)

# --- 2. Shared variables for the application state ---
whistle_count = 0
is_listening = False
audio_thread = None
amma_sound = AudioSegment.from_wav("amma_off_cooker.wav") # Make sure this file exists!

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
    global whistle_count, is_listening, amma_sound

    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    print("Audio stream started. Listening for whistles...")

    while is_listening:
        data = stream.read(CHUNK, exception_on_overflow=False)
        audio_data = np.frombuffer(data, dtype=np.int16)
        
        # --- Whistle Detection Logic (Your code goes here!) ---
        yf = rfft(audio_data)
        xf = rfftfreq(CHUNK, 1 / RATE)
        peak_frequency = xf[np.argmax(np.abs(yf))]
        peak_intensity = np.abs(yf[np.argmax(np.abs(yf))])

        if abs(peak_frequency - WHISTLE_FREQUENCY) < FREQUENCY_TOLERANCE and peak_intensity > WHISTLE_THRESHOLD:
            whistle_count += 1
            print(f"Whistle detected! Count: {whistle_count}")
            # --- Amma's voice logic ---
            if whistle_count == 3: # Change this number as needed
                print("Amma's voice playing!")
                play(amma_sound)
                whistle_count = 0 # Reset the counter

    # --- Clean up after listening stops ---
    stream.stop_stream()
    stream.close()
    p.terminate()
    whistle_count = 0 # Reset count when stopped

@app.route('/start_listening')
def start_listening():
    global is_listening, audio_thread, whistle_count
    if not is_listening:
        is_listening = True
        whistle_count = 0 # Reset count at the start
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