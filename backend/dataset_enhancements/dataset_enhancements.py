import librosa
import numpy as np
from transform_audio import normalize_audio, pitch_shift, time_stretch
from correct_mood import modify_mood


def get_spectrogram(y):
    """
    Get a spectrogram with 30 seconds of audio and a sr of 22050
    """
    sr = 22050
    max_duration = 30

    # Target length in samples (30 seconds)
    target_length = sr * max_duration  

    # Format the audio to a standard shape
    y = np.pad(y, (0, max(0, target_length - len(y))), mode='constant')[:target_length]
    # Generate a Mel spectrogram based on the audio
    S = librosa.feature.melspectrogram(y=y, sr=sr, n_mels=128, fmax=8000, dtype=np.float16)
    # Convert power to decibels
    S_db = librosa.power_to_db(S, ref=np.max)

    return S_db

def generate_new_data(y, corrected_mood_vector):
    """
    Apply transformations to the audio and generate corresponding spectrograms and mood vectors.
    """

    transformations = {
        # Original audio, normalized
        "normalized": (
            get_spectrogram(normalize_audio(y)),
            modify_mood(corrected_mood_vector, "normalize")
        ),
        
        # Pitch transformations
        "higher_pitch": (
            get_spectrogram(pitch_shift(y, n_steps=1.5)),
            modify_mood(corrected_mood_vector, "pitch_up")
        ),
        "lower_pitch": (
            get_spectrogram(pitch_shift(y, n_steps=-1.5)),
            modify_mood(corrected_mood_vector, "pitch_down")
        ),
        
        # Speed transformations
        "speed_up": (
            get_spectrogram(time_stretch(y, rate=1.1)),
            modify_mood(corrected_mood_vector, "speed_up")
        ),
        "slow_down": (
            get_spectrogram(time_stretch(y, rate=0.9)),
            modify_mood(corrected_mood_vector, "slow_down")
        )
    }
    
    return transformations







if __name__ == '__main__':
    mood = np.array([0.10579624262459593, 0.12441237013592801, 0.731041523983839, 0.09889122376391296, 0.08999753317332732, 0.6335693207859938, 0.095509896673731, 0.10244878084391208])


    print(mood)
