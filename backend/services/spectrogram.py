import requests
import librosa
import numpy as np
import tempfile
import torch


def generate_spectrogram(y, sr=22050, max_duration=30):
    # Target length in samples (30 seconds)
    target_length = sr * max_duration  

    # Format the audio to a standard shape (use y instead of audio)
    y = np.pad(y, (0, max(0, target_length - len(y))), mode='constant')[:target_length]

    # Generate a Mel spectrogram based on the formatted audio
    S = librosa.feature.melspectrogram(y=y, sr=sr, n_mels=128, fmax=8000, dtype=np.float16)

    # Convert power to decibels
    S_db = librosa.power_to_db(S, ref=np.max)
    
    S_db = np.array(S_db)

    return torch.FloatTensor(S_db).unsqueeze(0).unsqueeze(0)
        



__all__ = [generate_spectrogram.__name__]


    

 

