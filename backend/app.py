from flask import Flask, jsonify, request, session
from flask_cors import CORS
import torch
import services
from services import (load_model, get_song_preview, get_spectrogram_data, 
                      generate_spectrogram, get_moods_and_colors_from_mood_vector, 
                      generate_new_mood_vector)
import json

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'  # Required for session
CORS(app)

# Global variables for temporary storage
CURRENT_SPECTROGRAM = None
CURRENT_MOOD = None

# Init the model
model = load_model()

@app.get('/hello')
def hello():
    return jsonify({'message': 'Hello, world!'})

@app.get('/mood')
def predict_mood():
    global CURRENT_SPECTROGRAM, CURRENT_MOOD
    
    # Get the artist
    artist = request.args.get('artist')
    song = request.args.get('song')
    search_query = f"{song} {artist}"

    # Get the song preview
    audio_url = get_song_preview(search_query)

    if audio_url is None:
        return jsonify({'error': 'No audio URL found'}), 404
    
    # Get the spectrogram
    spectrogram = get_spectrogram_data(audio_url)
    CURRENT_SPECTROGRAM = spectrogram  # Store in memory instead of session
    
    # Get the mood prediction
    with torch.no_grad():
        mood = model(spectrogram)
        CURRENT_MOOD = mood.squeeze().squeeze()  # Store in memory instead of session

    moods_and_colors = get_moods_and_colors_from_mood_vector(CURRENT_MOOD)
    return jsonify(moods_and_colors)

@app.post('/correctmood')
def correct_mood():
    """
    A route in which the user can post corrected mood data and generate a new
    mood vector associated with the spectrogram
    """

    global CURRENT_MOOD
    try:
        # Get the correct moods
        correct_moods = request.get_json()['moods']
        
        # If there is no current mood, exit the post request
        if CURRENT_MOOD is None:
            return jsonify({'error': 'No mood data available'}), 400
        

        # Generate new, corrected mood vector  
        new_mood = generate_new_mood_vector(correct_moods, CURRENT_MOOD)

        return jsonify({'new_mood': new_mood.tolist()})  # Convert tensor/array to list
    
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
