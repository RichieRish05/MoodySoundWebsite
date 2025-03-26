import boto3
from botocore.exceptions import ClientError
import datetime
import csv

# Create the DynamoDB resource 
dynamodb = boto3.resource('dynamodb')

def enforce_keys(item):
    """
    Enforce the keys to the row of the table
    """
    required_keys = {
        'title',
        'artist',
        'spectrogram_file',
        'target_file',
        'comprehensive_mood',
        'timestamp'
    }

    missing_keys = required_keys - set(item.keys())

    if missing_keys:
        print(missing_keys)
        return False
    
    return True



def create_row(*, song_name, artist, spec_path, target_path, comprehensive_mood):
    # Create dictionary representing a row in the csv
    return {
        "spectrogram_file": spec_path,
        "target_file": target_path,
        "title": song_name,
        "artist": artist,
        "comprehensive_mood": comprehensive_mood,
        "timestamp": datetime.datetime.now().isoformat()
    }
    

def write_to_table(table_name, item):
    """
    A function to write an item to a specified dynamodb table
    """
    table = dynamodb.Table(table_name)

    if not enforce_keys(item):
        print('Missing keys')
        return False

    
    try:
        table.put_item(
            Item=item
        )
        print('Wrote to table successfully')
        return True
    except ClientError as e:
        print(f"Error writing to table: {e.response['Error']['Message']}")
        return False
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        return False


def get_items(table):
    response = table.scan()
    return response.get('Items', [])

def scan_table(table_name):
    """
    Function to scan all elements in the table
    """
    table = dynamodb.Table(table_name)
    count = 0
    
    # Retrieve all items in the table
    items = get_items(table)
    
    # Print out the items
    print(f"Items in table {table_name}:")
    for item in items:
        count += 1
        print(item)

    print(f'Count: {count}')
    
    return items

def export_table_to_s3_as_csv(table_name):
    """
    A function to take an entire dynamodb table and export it to s3 in the form
    of a csv
    """
    # Initialize the s3 client and get the table
    s3 = boto3.client('s3')
    table = dynamodb.Table(table_name)

    # Retrieve all items in the table
    items = get_items(table)

    headers = [
        'title',
        'artist',
        'spectrogram_file',
        'target_file',
        'comprehensive_mood',
        'timestamp'
    ]

    with open('metadata.csv', 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=headers)
        writer.writeheader()
        for item in items:
            writer.writerow(item)


def delete_item(table_name, key):
    """
    Function to delete an item from a dynamodb table
    """
    table = dynamodb.Table(table_name)
    
    # Delete the specified item using its primary key
    response = table.delete_item(Key=key)
    print(f"Deleted item with key: {key}")
    return response


    

__all__ = [write_to_table.__name__]



if __name__ == '__main__':
    scan_table('moodysoundtable')
