import random
import torch
import numpy as np

def normalize_mood(mood_vector):
    """
    Normalize the mood vector so it has a magnitude of 1
    """
    norm = np.linalg.norm(mood_vector)
    return mood_vector / norm

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
    return normalize_mood(new_mood_vector)


def modify_mood(mood_vector, transformation_type: str):
    """
    Modify the mood vector based on the specified transformation type.
    """

    # Make a copy to 
    mood_vector = np.array(mood_vector).copy()
    # Define mood positions for easy reference
    MOOD_POSITIONS = {
        'danceable': 0,
        'acoustic': 1,
        'aggressive': 2,
        'electric': 3,
        'happy': 4,
        'party': 5,
        'relaxed': 6,
        'sad': 7
    }

    # Define which moods to amplify for each transformation
    TRANSFORMATIONS = {
        'normalize': [],
        'pitch_up': ['happy', 'party'],
        'pitch_down': ['sad', 'relaxed'],
        'speed_up': ['danceable', 'party', 'happy'],
        'slow_down': ['sad', 'relaxed']
    }

    # Apply the transformation
    for mood in TRANSFORMATIONS[transformation_type]:
        mood_vector[MOOD_POSITIONS[mood]] = max(0.25, mood_vector[MOOD_POSITIONS[mood]] * 1.25)


    # Return normalized vector
    return normalize_mood(mood_vector)



if __name__ == '__main__':


    # Get the corrected mood vector
    corrected_mood_vector = np.array([0.055473766272003046, 0.5142119172134582, 0.04317293196632012, 0.0629753780371928, 0.04420166251078848, 0.03548774361120182, 0.5570629103145797, 0.6427648965168227])
    print(modify_mood(corrected_mood_vector, "pitch_up"))
