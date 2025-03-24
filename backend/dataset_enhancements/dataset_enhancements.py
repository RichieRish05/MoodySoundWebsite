import librosa
import numpy as np
from dataset_enhancements.transform_audio import normalize_audio, pitch_shift, time_stretch
from dataset_enhancements.correct_mood import modify_mood
from services import get_significant_moods
import boto3


def sanitize_song_name(song_name):
    """
    Clean the song name to be used as a file name
    """
    # Replace spaces with underscores
    song_name = song_name.strip().replace(' ', '_')

    invalid_characters = ['/', '\\',':', '*', '?', '"', '<', '>', '|' ]

    # Remove invalid characters
    sanitized_song_name = ''.join(char for char in song_name if char not in invalid_characters)


    return sanitized_song_name

def get_spectrogram(y):
    """
    Get a spectrogram with 30 seconds of audio and a standard sampling rate of 22050
    """
    sr = 22050
    max_duration = 30

    # Target length in samples (30 seconds)
    target_length = sr * max_duration  

    # Format the audio to a standard shape
    y = np.pad(y, (0, max(0, target_length - len(y))), mode='constant')[:target_length]
    # Generate a Mel spectrogram based on the audio
    S = librosa.feature.melspectrogram(y=y, sr=sr, n_mels=128, fmax=8000, dtype=np.float16)
    # Convert power to decibels
    S_db = librosa.power_to_db(S, ref=np.max)

    return S_db



def generate_new_data(artist, title, y, corrected_mood_vector):
    """
    Apply transformations to the audio and generate corresponding spectrograms and mood vectors.
    
        
    Yields:
        dict: Dictionary containing transformed audio data with keys:
            - name: String identifier for the transformation
            - spectrogram: Mel spectrogram of transformed audio
            - mood: Modified mood vector
    """

    # Define transformations as a list of tuples
    transformations = [
        ("normalized", normalize_audio, {}, "normalize"),
        ("pitch up", pitch_shift, {"n_steps": 1.5}, "pitch_up"),
        ("pitch down", pitch_shift, {"n_steps": -1.5}, "pitch_down"),
        ("speed up", time_stretch, {"rate": 1.1}, "speed_up"),
        ("slow down", time_stretch, {"rate": 0.9}, "slow_down")
    ]

    # Yield each transformation one at a time
    for suffix, transform_func, args, mood_type in transformations:
        try:
            transformed_audio = transform_func(y, **args)
            spectrogram = get_spectrogram(transformed_audio)
            mood = modify_mood(corrected_mood_vector, mood_type)
            comprehensive_mood = ', '.join(get_significant_moods(mood).keys())

            yield {
                "spectrogram_file_name": f"{sanitize_song_name(f'{title}_{artist}')}_{mood_type}_matrix.npy",
                "target_file_name": f"{sanitize_song_name(f'{title}_{artist}')}_{mood_type}_target.npy",
                "spectrogram": np.array(spectrogram),
                "mood": np.array(mood),
                "artist": artist,
                "title": f'{title}_{mood_type}',
                "comprehensive_mood": comprehensive_mood
            }
        except Exception as e:
            print(f"Failed to process {suffix} transformation: {str(e)}")
            continue


def upload_to_s3(file_name, bucket_name, object_name):
    """
    Upload a file to an S3 bucket
    """
    s3 = boto3.client('s3')
    s3.upload_file(
        Filename=file_name, 
        Bucket=bucket_name, 
        Key=object_name
    )




__all__ = [generate_new_data.__name__]

if __name__ == '__main__':
    # Get the audio url
    audio_url = "https://cdnt-preview.dzcdn.net/api/1/1/6/3/6/0/63676ab7820760a38a0a30c4cbfe43b1.mp3?hdnea=exp=1741767512~acl=/api/1/1/6/3/6/0/63676ab7820760a38a0a30c4cbfe43b1.mp3*~data=user_id=0,application_id=42~hmac=2b043d386a35f36e51a4b90611f9b95d701f74e2763c19ca9dc3838b9b908e03"
   

    y = get_audio(audio_url)
    mood = [0.5 for x in range(8)]

    for x in generate_new_data("Free Mind, Tems", y, mood):
        print(f"Name: {x['name']}")
        print(f"Spectrogram: {x['spectrogram'].shape}")
        print(f"Mood: {x['mood']}")




