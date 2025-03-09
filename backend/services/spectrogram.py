from services.song_preview import get_song_preview
import requests
import librosa
import numpy as np
import tempfile
import torch
import random


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
        spectrogram = generate_spectrogram(y_normalized)

        return spectrogram
    


def generate_spectrogram(y, sr=22050, min_duration=10, max_duration=30, step=10):
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
        

def get_random_low_value(num_moods_changed: int):
    """
    Get a random low value for the mood vector based on the number of moods changed.
    This is used to make insignificant moods have a lower value in the mood vector.
    """
    if num_moods_changed == 1:
        return random.uniform(0.1, 0.2)
    elif num_moods_changed == 2:
        return random.uniform(0.1, 0.15)
    elif num_moods_changed == 3:
        return random.uniform(0.05, 0.1)


def format_mood_representation(mood_representation: dict[str, int]):
    """
    Format the labels of the mood representation to match the labels of the data
    """


    mood_labels = {
        "Danceable": "danceable",
        "Acoustic": "mood_acoustic",
        "Aggressive": "mood_aggressive",
        "Electronic": "mood_electronic",
        "Happy": "mood_happy",
        "Party": "mood_party",
        "Relaxed": "mood_relaxed",
        "Sad": "mood_sad"
    }


    # Change the mood labels to reflect the labels used with the data
    return {place: mood_labels[mood] for place, mood in mood_representation.items() if mood is not None}




def generate_new_mood_vector(mood_representation: dict[str, int], predicted_mood: torch.Tensor):
    """
    Generate a new mood vector that more accurately represents a spectrogram
    based on user input mood representation and the old, predicted mood vector
    """

    # The positions of the moods in the mood vector
    MOOD_POSITIONS = [
        "danceable",
        "mood_acoustic",
        "mood_aggressive",
        "mood_electronic",
        "mood_happy",
        "mood_party",
        "mood_relaxed",
        "mood_sad"
    ]

    # Format the mood_representation
    mood_representation = format_mood_representation(mood_representation)


    # Get the number of moods changed 
    num_moods_changed = sum(1 for value in mood_representation.values() if value != None)
    # Generate a new mood vector with random, low values depending on num_moods_changed
    new_mood_vector = {mood: get_random_low_value(num_moods_changed) for mood in MOOD_POSITIONS}
    # Get the maximum value in the predicted mood vector
    MAXIMUM = float(torch.max(predicted_mood))




    # Manipulate the new mood vector to be more accurate
    for place, mood in mood_representation.items():
        if not mood:
            continue

        # Increase the corresponding mood value if it's dominant (value = 1, 2, 3)
        if place == '1':
            new_mood_vector[mood] = max(0.8, MAXIMUM * 1.5)
        elif place == '2':
            new_mood_vector[mood] = max(0.7, MAXIMUM * 1.3)
        elif place == '3':
            new_mood_vector[mood] = max(0.6, MAXIMUM * 1.2)


    

    # Convert the labeled mood vector into a numpy vector
    new_mood_vector = np.array(list(new_mood_vector.values()))



    # Normalize the mood vector
    norm = np.linalg.norm(new_mood_vector)
    normalized_mood_vector = new_mood_vector / norm



    return normalized_mood_vector



__all__ = [get_spectrogram_data.__name__, generate_spectrogram.__name__, generate_new_mood_vector.__name__]


if __name__ == "__main__":
    # Test the generate_new_mood_vector function
    mood_representation = {'1': 'Electronic', '2': 'Happy', '3': 'Sad'}
    

    mood_vector = torch.tensor([0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5])

    new_mood_vector = generate_new_mood_vector(mood_representation, mood_vector)

    print(new_mood_vector)
    



