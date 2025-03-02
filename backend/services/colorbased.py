import pandas as pd

# Define mood colors (RGB format)
MOOD_COLORS = {
    "mood_acoustic": (139, 69, 19),  # Brown
    "mood_aggressive": (255, 0, 0),  # Red
    "mood_electronic": (128, 0, 128),  # Purple
    "mood_happy": (255, 255, 0),  # Yellow
    "mood_party": (255, 165, 0),  # Orange
    "mood_relaxed": (0, 128, 0),  # Green
    "mood_sad": (0, 0, 255),  # Blue
}

def blend_colors(color1, color2):
    """Blend two RGB colors by averaging their components."""
    return tuple(int((c1 + c2) / 2) for c1, c2 in zip(color1, color2))

def get_top_two_moods(row):
    """Determine the top two moods and blend their colors."""
    mood_values = {mood: row[mood] for mood in MOOD_COLORS.keys() if mood in row}
    sorted_moods = sorted(mood_values.items(), key=lambda x: x[1], reverse=True)
    
    # Get the two highest moods
    if len(sorted_moods) >= 2:
        top_mood, top_value = sorted_moods[0]
        second_mood, second_value = sorted_moods[1]
    else:
        top_mood, top_value = sorted_moods[0]
        second_mood, second_value = None, None
    
    if second_mood:
        blended_color = blend_colors(MOOD_COLORS[top_mood], MOOD_COLORS[second_mood])
        return f"{top_mood} + {second_mood}", blended_color
    
    return top_mood, MOOD_COLORS[top_mood]

# Load the CSV file (ensure it contains the relevant mood sensor data)
df = pd.read_csv("torch_sensor_data.csv")

# Apply function to each row
df[["top_moods", "blended_color"]] = df.apply(lambda row: pd.Series(get_top_two_moods(row)), axis=1)

# Convert RGB tuples to hex colors
df["blended_color"] = df["blended_color"].apply(lambda rgb: "#{:02x}{:02x}{:02x}".format(*rgb))

# Save updated dataset
df.to_csv("updated_mood_sensor_data.csv", index=False)

# Display results
print(df[["top_moods", "blended_color"].head()])