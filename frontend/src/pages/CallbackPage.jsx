import { useEffect, useState } from 'react';
import SpotifyWebApi from 'spotify-web-api-js';

const getTokenFromUrl = () => {
    return window.location.hash
        .substring(1)
        .split('&')
        .reduce((initial, item) => {
            let parts = item.split('=');
            initial[parts[0]] = decodeURIComponent(parts[1]);
            return initial;
        }, {});
}

const parsePlaybackState = (playbackState) => {

    if (playbackState.currently_playing_type === 'track') {
        return {
            songName: playbackState.item.name,
            artistName: playbackState.item.artists.map((artist) => artist.name).join(', '),
            albumName: playbackState.item.album.name,
            imageUrl: playbackState.item.album.images[0].url,
        }
    }

    return null;
    
    
}

const fetchPlaybackState = async (spotifyApi) => {
    let res = await spotifyApi.getMyCurrentPlaybackState();
    res = parsePlaybackState(res)

    return res;
}






const CallbackPage = () => {
    const spotifyApi = new SpotifyWebApi();
    const [spotifyToken, setSpotifyToken] = useState(null);
    const [playbackState, setPlaybackState] = useState(null);

    
    
    useEffect(() => {
        const tokens = getTokenFromUrl();
        if (tokens.access_token) {
            setSpotifyToken(tokens.access_token);
            spotifyApi.setAccessToken(tokens.access_token);

            const intervalId = setInterval(async () => {
                const playbackState = await fetchPlaybackState(spotifyApi);
                setPlaybackState(playbackState);
                console.log(playbackState);
            }, 1000);

            return () => clearInterval(intervalId);
        }


    }, [spotifyToken])





    return (
        <div>
            <h1>Welcome</h1>
            {playbackState && (
                <div>
                    <img src={playbackState.imageUrl} alt="album cover" />
                    <h2>{playbackState.songName}</h2>
                    <h3>{playbackState.artistName}</h3>
                    <h4>{playbackState.albumName}</h4>
                </div>
            )}

        </div>
    )
}

export default CallbackPage;