import numpy as np
from dataset_enhancements.transform_audio import get_audio, normalize_audio, pitch_shift, time_stretch
from dataset_enhancements.correct_mood import modify_mood
from dataset_enhancements.dataset_enhancements import generate_new_data
import sounddevice as sd
from services import get_song_preview

# Get the audio url from the search query
query = 'Higher, Tems'
audio_url = get_song_preview(query)
# Get the audio from the search query
audio = get_audio(audio_url)




# Get the corrected mood vector
corrected_mood_vector = np.array([0.055473766272003046, 0.5142119172134582, 0.04317293196632012, 0.0629753780371928, 0.04420166251078848, 0.03548774361120182, 0.5570629103145797, 0.6427648965168227])




def playAudio(y):
    sd.play(y,samplerate=22050)
    sd.wait()


def test_audio():
    print('Normalized')
    print(modify_mood(corrected_mood_vector, "normalize"))
    playAudio(normalize_audio(audio))

    print('\nPitch Shifted Up')
    print(modify_mood(corrected_mood_vector, "pitch_up"))
    playAudio(pitch_shift(audio, 1.5))

    print('\nPitch Shifted Down')
    print(modify_mood(corrected_mood_vector, "pitch_down"))
    playAudio(pitch_shift(audio, -1.5))

    print('\nTime Stretched Faster')
    print(modify_mood(corrected_mood_vector, "speed_up"))
    playAudio(time_stretch(audio, 1.1))

    print('\nTime Stretched Slower')
    print(modify_mood(corrected_mood_vector, "slow_down"))
    playAudio(time_stretch(audio, 0.9))

def test_spectrograms():
    transformations = generate_new_data(audio, corrected_mood_vector)

    for key, (spectrogram, mood) in transformations.items():
        print(query+key)
        print(spectrogram.shape)
        print(mood)


test_spectrograms()


