import numpy as np
import tempfile
import boto3
from dataset_enhancements.table import create_row, write_to_table


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
                Bucket='rishitestbucket01',
                Key=f'data/targets/{file_name}'
            )
        
        print('Uploaded mood successfully')
        return True
    except Exception as e:
        print(f"Error uploading spectrogram to S3: {str(e)}")
        return False




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
                Bucket='rishitestbucket01',
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
    for x in transformations:
        try:
            # print(f"Spectrogram: {x['spectrogram']}")
            # print(f"Mood: {x['mood']}")3
            row = create_row(
                artist= x['artist'],
                song_name= x['title'],
                spec_path= x['spectrogram_file_name'],
                target_path= x['target_file_name'],
                comprehensive_mood=x['comprehensive_mood']
            )
            
            write_to_table('TestMoodySoundTable', row)
            upload_spec_to_s3(s3_client=s3, file_name=x['spectrogram_file_name'], spec=x['spectrogram'])
            upload_mood_to_s3(s3_client=s3, file_name=x['target_file_name'], mood=x['mood'])
        except Exception as e:
            print(f"Error processing transformation: {str(e)}")
            continue


__all__ = [process_transformations.__name__]