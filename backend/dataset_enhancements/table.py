import boto3
from botocore.exceptions import ClientError

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
        'comprehensive_mood'
    }

    missing_keys = required_keys - set(item.keys())

    if missing_keys:
        print(missing_keys)
        return False
    
    return True



def create_row(*, song_name, artist, spec_path, target_path, comprehensive_mood):
    # Create dictionary representing a row in the csv
    return {
        "title": song_name,
        "artist": artist,
        "spectrogram_file": spec_path,
        "target_file": target_path,
        "comprehensive_mood": comprehensive_mood
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


def scan_table(table_name):
    """
    Function to scan all elements in the table
    """
    table = dynamodb.Table(table_name)
    
    # Retrieve all items in the table
    response = table.scan()
    items = response.get('Items', [])
    
    # Print out the items
    print(f"Items in table {table_name}:")
    for item in items:
        print(item)
    
    return items

def delete_item(table_name, key):
    """
    Function to delete an item from a dynamodb table
    """
    table = dynamodb.Table(table_name)
    
    # Delete the specified item using its primary key
    response = table.delete_item(Key=key)
    print(f"Deleted item with key: {key}")
    return response


__all__ = [write_to_table.__name__, ]
if __name__ == '__main__':
    table_name = 'TestMoodySoundTable'
    
    # List all items in the table
    items = scan_table(table_name)
    
    # Example: delete an item with primary key 'id' equal to '123'
    # key_to_delete = {'id': '123'}
    # delete_item(table_name, key_to_delete)


