import numpy as np
import tempfile
import boto3
from dataset_enhancements.table import create_row, write_to_table
from dotenv import load_dotenv
import os
import time

load_dotenv()

def with_retries(n, delay = 1):
    """
    Retry a function n times with exponential backoff.
    """
    def decorate(func):
        def run(*args, **kwargs):
            for i in range(n-1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    time.sleep(delay * (2 ** i))  # Exponential backoff
                    continue
            return func(*args, **kwargs)
        return run
    return decorate
    




@with_retries(3)
def upload_mood_to_s3(s3_client, file_name, mood):
    """
    A function to upload moods to the s3 bucket
    """
    try:
        with tempfile.NamedTemporaryFile(suffix='.npy', delete=True) as f:
            # Save the mood to the temporary file
            np.save(f.name, mood)
            f.flush()  # Ensure all data is written to disk

            # Upload the file to S3
            s3_client.upload_file(
                Filename=f.name,
                Bucket=os.getenv('S3_BUCKET_NAME'),
                Key=f'data/targets/{file_name}'
            )
        
        print('Uploaded mood successfully')
        return True
    except Exception as e:
        print(f"Error uploading spectrogram to S3: {str(e)}")
        return False



@with_retries(3)
def upload_spec_to_s3(s3_client, file_name, spec):
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
                Bucket=os.getenv('S3_BUCKET_NAME'),
                Key=f'data/spectrograms/{file_name}'
            )
        
        print('Uploaded spectrogram succesfully')
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
    # Track the last processed transformation
    
    for x in transformations:
        try:
            row = create_row(
                artist=x['artist'],
                song_name=x['title'],
                spec_path=x['spectrogram_file_name'],
                target_path=x['target_file_name'],
                comprehensive_mood=x['comprehensive_mood']
            )
            
            upload_spec_to_s3(s3_client=s3, file_name=x['spectrogram_file_name'], spec=x['spectrogram'])
            upload_mood_to_s3(s3_client=s3, file_name=x['target_file_name'], mood=x['mood'])
            write_to_table(os.getenv('CSV_TABLE_NAME'), row)
        except Exception as e:
            print(f"Error processing transformation: {str(e)}")
            continue



def get_dominant_mood(mood_vector):
    MOOD_POSITIONS = {
        0: "danceable",
        1: "mood_acoustic",
        2: "mood_aggressive",
        3: "mood_electronic",
        4: "mood_happy",
        5: "mood_party",
        6: "mood_relaxed",
        7: "mood_sad"
    }

    max_index = None
    max = -float('inf')

    for i in range(1, len(mood_vector)): # Ignore danceable because it blends with too many moods well
        if mood_vector[i] > max:
            max = mood_vector[i]
            max_index = i
    
    return MOOD_POSITIONS[max_index]


def handle_transformations_and_uploads(transformations, title, artist, mood_vector):
    process_transformations(transformations)

    # Write to the query table
    write_to_table(os.getenv('QUERY_TABLE_NAME'), item={
        'title': title,
        'artist': artist,
        'dominant_mood': get_dominant_mood(mood_vector)
    })
    print(title)
    print(artist)
    print(get_dominant_mood(mood_vector))


    




__all__ = [handle_transformations_and_uploads.__name__]