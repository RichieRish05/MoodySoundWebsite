import boto3
from dotenv import load_dotenv
import os 
import random

# Initialize DynamoDB resource once at module level
dynamodb = boto3.resource('dynamodb', region_name='us-west-2')

def select_song_that_matches_mood(table_name, significant_moods):
    """
    Function that queries a DynamoDB table for a single random song matching any of the significant moods
    """
    table = dynamodb.Table(table_name)

    for mood in significant_moods:
        response = table.query(
            IndexName='DominantMoodIndex',
            KeyConditionExpression='dominant_mood = :mood',
            Limit=100,  # Get a batch of songs to choose from
            ExpressionAttributeValues={
                ':mood': mood
            }
        )
        matched_songs = response.get('Items', [])

        if matched_songs:
            return random.choice(matched_songs)
    
    return None


__all__ = [select_song_that_matches_mood.__name__]


if __name__ == '__main__':
    # significant_moods = ['danceable', 'happy']
    # print(create_filter_expression(significant_moods))
    # print(create_expression_values(significant_moods))


    load_dotenv()
    print(select_song_that_matches_mood(os.getenv('QUERY_TABLE_NAME'), ['mood_happy', 'mood_sad']))