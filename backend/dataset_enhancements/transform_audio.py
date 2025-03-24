import requests
import librosa
import tempfile

    

def normalize_audio(y):
    """
    Normalize the audio from [-1,1]
    """
    return librosa.util.normalize(y)

def pitch_shift(y, n_steps=0):
    """
    Shift the pitch of audio by n steps
    """
    y_shifted = librosa.effects.pitch_shift(y, sr=22050, n_steps=n_steps)
    return normalize_audio(y_shifted)

def time_stretch(y, rate=1): 
    """
    Speed a song up or slow it down based on rate
    """
    y_stretched = librosa.effects.time_stretch(y, rate=rate)
    return normalize_audio(y_stretched)



__all__ = [
    normalize_audio.__name__, 
    pitch_shift.__name__, 
    time_stretch.__name__
]