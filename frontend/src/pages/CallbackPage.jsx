import { useEffect, useState } from 'react';
import SpotifyWebApi from 'spotify-web-api-js';
import axios from 'axios';


const BACKEND_URL = import.meta.env.VITE_BACKEND_URL 

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
    const [mood, setMood] = useState(null);
    
    
    useEffect(() => {
        const tokens = getTokenFromUrl();
        if (tokens.access_token) {
            setSpotifyToken(tokens.access_token);
            spotifyApi.setAccessToken(tokens.access_token);

            const intervalId = setInterval(async () => {
                const newPlaybackState = await fetchPlaybackState(spotifyApi);
                if (newPlaybackState !== playbackState) {
                    setPlaybackState(newPlaybackState);
                    console.log(newPlaybackState);
                }
            }, 1000);

            return () => clearInterval(intervalId);
        }

    }, [spotifyToken])


    useEffect(() => {
        console.log('ACCESSED MOOD CHANGE');

        const fetchMood = async (songName, artistName) => {
            const mood = await axios.get(`${BACKEND_URL}/mood?song=${songName}&artist=${artistName}`)
                .then((res) => {
                    console.log(res.data.mood);
                    return res.data.mood;
                })
                .catch((err) => {
                    console.error(err);
                    return null;
                });

            return mood;
        }

        if (playbackState) {
            const mood = fetchMood(playbackState.songName, playbackState.artistName)
            if (mood) {
                setMood(mood);
            }
        }
    }, [playbackState])





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