from flask import Flask, jsonify, request
from flask_cors import CORS
import torch
import services
import dataset_enhancements
import threading
import librosa

app = Flask(__name__)
CORS(app)

# Init the model
model = services.load_model()

@app.get('/hello')
def hello():
    return jsonify({'message': 'Hello, world!'})

@app.get('/mood')
def predict_mood():
    # Get the artist
    artist = request.args.get('artist')
    song = request.args.get('song')
    search_query = f"{song}, {artist}"

    # Get the song preview
    audio_url = services.get_song_preview(search_query)

    if audio_url is None:
        return jsonify({'error': 'No audio URL found'}), 404
    
    # Get the audio from the audio url
    audio = services.get_audio(audio_url)
    # Normalize the audio waveform to a range of [-1, 1].
    audio = librosa.util.normalize(audio)
    # Generate the spectrogram
    spectrogram = services.generate_spectrogram(audio)
    # Get the mood prediction vector as a list
    with torch.no_grad():
        mood = model(spectrogram).squeeze().tolist()
        
    

    song_info = services.get_moods_and_colors_from_mood_vector(mood)
    song_info["search_query"] = search_query
    song_info["title"] = song
    song_info["artist"] = artist

    # Return the moods, colors, and song information
    return jsonify(song_info)




@app.post('/correctmood')
def correct_mood():
    """
    A route in which the user can post corrected mood data and generate a new
    mood vector associated with the spectrogram
    """

    try:
        # Get the correct moods
        correct_moods = request.get_json()['moods']
        vector = request.get_json()['vector']
        song_info = request.get_json()['songInfo']
        title = request.get_json()['title']
        artist = request.get_json()['artist']

        # Get the audio url
        audio_url = services.get_song_preview(song_info)
        
        # If there is no current mood, exit the post request
        if audio_url is None:
            return jsonify({'error': 'No mood data available'}), 400
        
        # Generate new, corrected mood vector  
        new_mood = dataset_enhancements.generate_new_mood_vector(correct_moods, vector).tolist()
        # Get just the audio
        audio = services.get_audio(audio_url) 

        # Create the new data generator
        transformations = dataset_enhancements.generate_new_data(artist, title, audio, new_mood)
        
        # Start uploading data in a separate thread
        thread = threading.Thread(target=dataset_enhancements.process_transformations, args=(transformations,))
        thread.start()

        return jsonify({'new_mood': new_mood}) 
    
    except Exception as e:
        return jsonify({'error': str(e)}), 400


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
