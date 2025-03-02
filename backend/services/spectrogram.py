from services.song_preview import get_song_preview
import requests
import librosa
import numpy as np
import tempfile
import torch




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

    # Format the audio to a standard shape (use y instead of audio)
    y = np.pad(y, (0, max(0, target_length - len(y))), mode='constant')[:target_length]

    # Generate a Mel spectrogram based on the sliced audio
    S = librosa.feature.melspectrogram(y=y, sr=sr, n_mels=128, fmax=8000, dtype=np.float16)

    # Convert power to decibels
    S_db = librosa.power_to_db(S, ref=np.max)
    
    S_db = np.array(S_db)

    return torch.FloatTensor(S_db).unsqueeze(0).unsqueeze(0)
        





__all__ = [get_spectrogram_data.__name__, get_spectrogram.__name__]




