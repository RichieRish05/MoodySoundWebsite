from flask import Flask, jsonify, request
from flask_cors import CORS
import torch
import services
import dataset_enhancements

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
    audio_url = services.get_song_preview(search_query) #

    if audio_url is None:
        return jsonify({'error': 'No audio URL found'}), 404
    
    # Get the spectrogram
    spectrogram = services.get_spectrogram_data(audio_url) # instead of passing audio url, pass audio itself
    
    # Get the mood prediction as a list
    with torch.no_grad():
        mood = model(spectrogram).squeeze().tolist()
        
    

    song_info = services.get_moods_and_colors_from_mood_vector(mood)
    song_info["search_query"] = search_query


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

        # Get the audio url
        audio_url = services.get_song_preview(song_info)
        
        # If there is no current mood, exit the post request
        if audio_url is None:
            return jsonify({'error': 'No mood data available'}), 400
        

        # Generate new, corrected mood vector  
        new_mood = dataset_enhancements.generate_new_mood_vector(correct_moods, vector).tolist()
        # Get just the audio
        audio = dataset_enhancements.get_audio(audio_url) # Move this into services



        # Generate the data here and see if everything is ok
        transformations = dataset_enhancements.generate_new_data(song_info, audio, new_mood)

        try: 
            for x in transformations:
                print(f"Name: {x['name']}")
                print(f"Spectrogram: {x['spectrogram'].shape}")
                print(f"Mood: {x['mood']}")
        except Exception as e:
            print(str(e))
            

        

        return jsonify({'new_mood': new_mood}) 
    
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
