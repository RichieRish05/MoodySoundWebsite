from services.song_preview import get_song_preview
import requests
import librosa
import numpy as np
import tempfile




def get_spectrogram_data(audio_url, sr=22050, duration=30):
    #Download the audio file
    response = requests.get(audio_url)

    # Save the file temporarily
    with tempfile.NamedTemporaryFile(delete=True, suffix=".mp3") as temp_audio_file:
        # Write the content of the audio file to the temporary file
        temp_audio_file.write(response.content)

        # Create a fake path for librosa to work with
        temp_audio_path = temp_audio_file.name

        # Load the temporary file with a predetermined sampling rate and a duration of 30 seconds to preprocess data
        y, _ = librosa.load(temp_audio_path, sr=sr, duration=duration)

        # Normalize the audio waveform to a range of [-1, 1].
        y_normalized = librosa.util.normalize(y)

        # Obtain 3 spectograms that contain audio samples of 10s, 20s, and 30s
        spectrogram = get_spectrogram(y_normalized)

        return spectrogram
    


def get_spectrogram(y, sr=22050, min_duration=10, max_duration=30, step=10):

    # Target length in samples (30 seconds)
    target_length = sr * max_duration  


    # Format the audio to a standard shape
    audio = np.pad(audio, (0, max(0, target_length - len(audio))), mode='constant')[:target_length]

    # Generate a Mel spectrogram based on the sliced audio
    S = librosa.feature.melspectrogram(y=audio, sr=sr, n_mels=128, fmax=8000, dtype=np.float16)

    # Convert power to decibels
    S_db = librosa.power_to_db(S, ref=np.max)

    
    return np.array(S_db)
        





__all__ = [get_spectrogram_data.__name__, get_spectrogram.__name__]


"""
#Search for the audio file
audio_url = get_song_preview("Hello")
print(audio_url)

spectrograms = get_spectrogram_data(audio_url)

for s in spectrograms:
    print(s.shape)


import sounddevice as sd

sd.play(audio, samplerate=sr)
sd.wait()  # Wait until the audio finishes playing
"""


