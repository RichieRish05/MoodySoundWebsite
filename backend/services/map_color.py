import pandas as pd
import torch
from collections import namedtuple
from webcolors import rgb_to_hex

# Define mood colors (RGB format)
MOOD_COLORS = {
    "danceable":       (177, 156, 217),  # Magenta
    "mood_acoustic":   (160,  82,  45),  # Sienna
    "mood_aggressive": (220,  20,  60),  # Crimson
    "mood_electronic": (  0, 255, 255),  # Cyan
    "mood_happy":      (255, 223,   0),  # Bright Yellow
    "mood_party":      (255, 0, 147),  # Deep Pink
    "mood_relaxed":    ( 34, 139,  34),  # Forest Green
    "mood_sad":        ( 30, 144, 255),  # Dodger Blue
}



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



def get_top_two_moods(mood_vector: torch.Tensor):
    # Convert mood vector to dictionary
    mood = {label: float(value) for label, value in zip(MOOD_POSITIONS, mood_vector)}

    # Create a namedtuple to store mood label and value
    Mood = namedtuple('Mood', ['label', 'value'])

    # Initialize greatest and second greatest moods
    greatest_mood = Mood(label=None, value=float('-inf'))
    second_greatest_mood = Mood(label=None, value=float('-inf'))

    # Iterate through moods and update greatest and second greatest moods
    for mood, value in mood.items():
        if value > greatest_mood.value:
            second_greatest_mood = greatest_mood
            greatest_mood = Mood(label=mood, value=value)
        elif value > second_greatest_mood.value:
            second_greatest_mood = Mood(label=mood, value=value)

    return greatest_mood, second_greatest_mood



def get_moods_and_colors_from_mood_vector(mood_vector: torch.Tensor) -> dict:
    greatest_mood, second_greatest_mood = get_top_two_moods(mood_vector)

    weight1 = max(greatest_mood.value*2, 0.5)
    weight2 = max(second_greatest_mood.value*2, 0.5)


    # If one of the moods is aggressive, return red
    if greatest_mood.label == "mood_aggressive" or second_greatest_mood.label == "mood_aggressive":
        return {
            "moods": [greatest_mood.label, second_greatest_mood.label],
            "color": rgb_to_hex((255, 0, 0)),
            "vector": mood_vector.tolist()
        }


    # Return the weighted, blended color of the two moods and the moods themselves
    return {
        "moods": [greatest_mood.label, second_greatest_mood.label],
        "color": rgb_to_hex(blend_colors(MOOD_COLORS[greatest_mood.label], MOOD_COLORS[second_greatest_mood.label], weight1, weight2)),
        "vector": mood_vector.tolist()
    }


def blend_colors(color1, color2, weight1, weight2):
    """Blend two RGB colors by averaging their components."""
    return tuple(int((c1 * weight1 + c2 * weight2) / (weight1 + weight2)) for c1, c2 in zip(color1, color2))




__all__ = [get_moods_and_colors_from_mood_vector.__name__]