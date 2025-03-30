import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import os

def create_spotify_client():
    """
    Create an authenticated Spotify client using credentials
    
    Returns:
        spotipy.Spotify: Authenticated Spotify client
    """
    client_id = os.getenv('SPOTIFY_CLIENT_ID')
    client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')
    
    if not client_id or not client_secret:
        raise ValueError("Spotify credentials not found in environment variables")
    
    # Create client credentials manager
    auth_manager = SpotifyClientCredentials(
        client_id=client_id,
        client_secret=client_secret
    )
    
    # Create Spotify client with auth manager
    return spotipy.Spotify(client_credentials_manager=auth_manager)

def get_track_album_cover_by_search(track_name: str, artist_name: str) -> tuple[str, str]:
    """
    Get the album cover URL and Spotify track URL for a track by searching with track name and artist
    """
    try:
        # Get authenticated client
        spotify = create_spotify_client()
        
        # Search for the track
        query = f"track:{track_name} artist:{artist_name}"
        results = spotify.search(q=query, type='track', limit=1)
        
        if results['tracks']['items']:
            track = results['tracks']['items'][0]
            images = track['album']['images']
            external_urls = track['external_urls']
            
            if images and external_urls:
                return {
                    'album_cover': images[0]['url'], 
                    'url': external_urls['spotify']
                }
                
        return None
        
    except Exception as e:
        print(f"Error getting album cover: {str(e)}")
        return None


__all__ = [get_track_album_cover_by_search.__name__]

if __name__ == '__main__':
    from dotenv import load_dotenv
    load_dotenv()

    print(get_track_album_cover_by_search("God's Plan", "Drake"))