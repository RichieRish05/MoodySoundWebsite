from flask import Flask, jsonify, request
from flask_cors import CORS
import torch
from services import load_model, get_song_preview, get_spectrogram_data, generate_spectrogram, get_moods_and_colors_from_mood_vector

app = Flask(__name__)
CORS(app)


CURRENT_SPECTROGRAM = None
CURRENT_MOOD = None

# Init the model
model = load_model()

@app.get('/hello')
def hello():
    return jsonify({'message': 'Hello, world!'})


@app.get('/mood')
def predict_mood():
    # Get the artist
    artist = request.args.get('artist')
    song = request.args.get('song')
    search_query = f"{song} {artist}"


    # Get the song preview
    audio_url = get_song_preview(search_query)




    # Get the spectrogram
    if audio_url is None:
        return jsonify({'error': 'No audio URL found'}), 404
    
    # Get the spectrogram
    spectrogram = get_spectrogram_data(audio_url)
    CURRENT_SPECTROGRAM = spectrogram


    # Get the mood prediction
    with torch.no_grad():
        mood = model(spectrogram)

    CURRENT_MOOD = mood.squeeze().squeeze()
    print(CURRENT_MOOD)


    moods_and_colors = get_moods_and_colors_from_mood_vector(CURRENT_MOOD)

    return jsonify(moods_and_colors)





if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)


@app.post('/correctmood')
def correct_mood():
    data = request.json
    moods = data.get('moods')

    sorted_moods = sorted(moods, key=lambda x: x[1], reverse=True)

    


    # Add the mood to the dataset


    return jsonify({'message': 'Added to dataset'})
