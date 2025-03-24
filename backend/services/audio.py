import requests
import librosa
import tempfile

def get_audio(audio_url):
    """
    Get audio from the audio link
    """
    #Download the audio file
    response = requests.get(audio_url)

    # Save the file temporarily
    with tempfile.NamedTemporaryFile(delete=True, suffix=".mp3") as temp_audio_file:
        # Write the content of the audio file to the temporary file
        temp_audio_file.write(response.content)

        # Create a fake path for librosa to work with
        temp_audio_path = temp_audio_file.name

        # Load the temporary file with a predetermined sampling rate and a duration of 30 seconds to preprocess data
        y, _ = librosa.load(temp_audio_path, sr=22050, duration=30)

        # Return the audio
        return y
    
__all__ = [get_audio.__name__]