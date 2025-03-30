import torch
from webcolors import rgb_to_hex



# Define mood colors (RGB format)
MOOD_COLORS = {
    "danceable":       (147,  51, 255),  # Bright Purple
    "mood_acoustic":   ( 41, 128, 185),  # Bright Orange
    "mood_aggressive": (255,   0,   0),  # Pure Red
    "mood_electronic": (255, 136,   0),  # Turquoise
    "mood_happy":      (255, 221,   0),  # Golden Yellow
    "mood_party":      (255,   0, 255),  # Hot Pink
    "mood_relaxed":    ( 76, 217,  76),  # Lime Green
    "mood_sad":        (  0, 128, 255),  # Bright Blue
}


# TRY TAKING ANYTHING ABOVE 0.3 AS A MAJOR MOOD


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



def get_significant_moods(mood_vector: list):
    MAX_VALUE = max(mood_vector)
    THRESHOLD = MAX_VALUE * 0.75

    # Convert mood vector to dictionary and filter by threshold
    significant_moods = {label: value for label, value in zip(MOOD_POSITIONS, mood_vector) if value > THRESHOLD}
    
    # Sort moods by value and take top 3
    sorted_moods = sorted(significant_moods.items(), key=lambda x: x[1], reverse=True)
    top_3_moods = dict(sorted_moods[:3])

    # If both happy and sad are in the significant moods, remove the one with the lower value
    if 'mood_happy' in top_3_moods and 'mood_sad' in top_3_moods:
        mood_happy_value = top_3_moods['mood_happy']
        mood_sad_value = top_3_moods['mood_sad']

        if mood_happy_value > mood_sad_value:
            top_3_moods.pop('mood_sad')
        else:
            top_3_moods.pop('mood_happy')

    return top_3_moods




def get_moods_and_colors_from_mood_vector(mood_vector: list) -> dict:
    significant_moods = get_significant_moods(mood_vector)


    # Return the weighted, blended color of the two moods and the moods themselves
    return {
        "significant_moods": list(significant_moods.keys()),
        "color": rgb_to_hex(blend_colors(significant_moods)),
        "vector": mood_vector
    }


def blend_colors(moods):
    """Blend significant moods while preserving color vibrancy."""
    if len(moods) == 1:
        return MOOD_COLORS[list(moods.keys())[0]]
    
    weights = [0.7, 0.3, 0.2, 0.1, 0.1, 0.1, 0.1, 0.1]

    blended_color = [0,0,0]
    for mood, index in zip(moods.keys(), range(len(moods))):
        for i in range(3):
            blended_color[i] += MOOD_COLORS[mood][i] * weights[index]

    return tuple(int(c) for c in blended_color)


    




__all__ = [get_moods_and_colors_from_mood_vector.__name__, get_significant_moods.__name__]


if __name__ == "__main__":
    print(get_moods_and_colors_from_mood_vector(torch.tensor([0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5])))
