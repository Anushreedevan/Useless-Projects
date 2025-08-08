# File: convert_audio.py

import os
from pydub import AudioSegment

# --- Add this line to tell pydub where to find FFmpeg ---
# Use the correct path to your FFmpeg bin folder
os.environ["PATH"] += os.pathsep + r"C:\Users\Aparna\Downloads\ffmpeg-7.1.1-essentials_build\ffmpeg-7.1.1-essentials_build\bin"

try:
    # Load the opus file
    # Make sure your file is named 'amma_off_cooker.opus'
    opus_file = AudioSegment.from_file("amma_off_cooker.opus", format="opus")

    # Export it as a WAV file
    opus_file.export("amma_off_cooker.wav", format="wav")

    print("File successfully converted to 'amma_off_cooker.wav'!")
except FileNotFoundError:
    print("Error: The file 'amma_off_cooker.opus' was not found in the project folder.")
    