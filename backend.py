# File: backend.py

import pyaudio
import numpy as np

# Audio settings
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100

def listen_to_mic():
    """Sets up and starts listening to the microphone."""
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    print("Listening for audio... Press Ctrl+C to stop.")

    try:
        while True:
            # Read a chunk of audio data
            data = stream.read(CHUNK)
            # Convert to numpy array for processing later
            audio_data = np.frombuffer(data, dtype=np.int16)
            # We will add whistle detection logic here later
            # For now, we can just print a dot to show it's working
            # print(".", end="", flush=True)

    except KeyboardInterrupt:
        print("\nStopping audio stream.")

    finally:
        # Stop and close the stream
        stream.stop_stream()
        stream.close()
        p.terminate()

if __name__ == "__main__":
    listen_to_mic()