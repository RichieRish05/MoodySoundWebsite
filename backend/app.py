from flask import Flask, jsonify, request
from flask_cors import CORS
import torch
from services import load_model, get_song_preview, get_spectrogram_data, get_spectrogram, get_moods_and_colors_from_mood_vector

app = Flask(__name__)
CORS(app)


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

    # Get the mood prediction
    with torch.no_grad():
        mood = model(spectrogram)


    moods_and_colors = get_moods_and_colors_from_mood_vector(mood.squeeze().squeeze())
    print(moods_and_colors)

    return jsonify(moods_and_colors)





if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
