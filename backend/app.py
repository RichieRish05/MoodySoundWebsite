from flask import Flask, jsonify, request
from flask_cors import CORS
import torch
import services
import dataset_enhancements
import threading
import boto3
import tempfile
import numpy as np

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

def upload_mood_to_s3(s3_client, song_name, mood):
    """
    A function to upload a mood to the s3 bucket
    """
    try:
        with tempfile.NamedTemporaryFile(suffix='.npy', delete=True) as f:
            # Save the mood to the temporary file
            np.save(f.name, mood)
            f.flush()  # Ensure all data is written to disk

            # Upload the file to S3
            s3_client.upload_file(
                Filename=f.name,
                Bucket='rishitestbucket01',
                Key=f'data/targets/{song_name}_target.npy'
            )
        return True
    except Exception as e:
        print(f"Error uploading spectrogram to S3: {str(e)}")
        return False




def upload_spec_to_s3(s3_client, song_name, spec):
    """
    A function to upload spectrograms to the s3 bucket
    """
    try:
        with tempfile.NamedTemporaryFile(suffix='.npy', delete=True) as f:
            # Save the spectrogram to the temporary file
            np.save(f.name, spec)
            f.flush()  # Ensure all data is written to disk

            # Upload the file to S3
            s3_client.upload_file(
                Filename=f.name,
                Bucket='rishitestbucket01',
                Key=f'data/spectrograms/{song_name}_matrix.npy'
            )
        return True
    except Exception as e:
        print(f"Error uploading spectrogram to S3: {str(e)}")
        return False
    


def process_transformations(transformations):
    """
    A function to asynchronously process the new spectrogram
    data and upload to s3
    """
    s3 = boto3.client('s3')
    try:
        for x in transformations:
            print(f"Name: {x['name']}")
            print(f"Spectrogram: {x['spectrogram'].shape}")
            print(f"Mood: {x['mood']}")
            upload_spec_to_s3(s3_client=s3, song_name=x['name'], spec=x['spectrogram'])
            upload_mood_to_s3(s3_client=s3, song_name=x['name'], mood=x['mood'])
    except Exception as e:
        print(str(e))

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



        # Create the new data generator
        transformations = dataset_enhancements.generate_new_data(song_info, audio, new_mood)
        
        # Start processing transformations in a separate thread
        thread = threading.Thread(target=process_transformations, args=(transformations,))
        thread.start()

        return jsonify({'new_mood': new_mood}) 
    
    except Exception as e:
        return jsonify({'error': str(e)}), 400


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
