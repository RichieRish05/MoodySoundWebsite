import { useEffect, useState } from 'react';
import SpotifyWebApi from 'spotify-web-api-js';
import axios from 'axios';
import './CallbackPage.css';

const BACKEND_URL = import.meta.env.VITE_BACKEND_URL 

interface PlaybackState {
    songName: string;
    artistName: string;
    albumName: string;
    imageUrl: string;
}

interface TokenResponse {
    access_token?: string;
    [key: string]: string | undefined;
}

const getTokenFromUrl = (): TokenResponse => {
    return window.location.hash
        .substring(1)
        .split('&')
        .reduce((initial, item) => {
            let parts = item.split('=');
            initial[parts[0]] = decodeURIComponent(parts[1]);
            return initial;
        }, {});
}

const parsePlaybackState = (playbackState: any): PlaybackState | null => {

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

const fetchPlaybackState = async (spotifyApi: SpotifyWebApi.SpotifyWebApiJs): Promise<PlaybackState | null> => {
    let res = await spotifyApi.getMyCurrentPlaybackState();
    res = parsePlaybackState(res)

    return res;
}


const arePlaybackStatesEqual = (state1: PlaybackState | null, state2: PlaybackState | null): boolean => {
    // If both states are null, they're equal
    if (state1 === null && state2 === null) return true;
    // If only one state is null, they're not equal
    if (state1 === null || state2 === null) return false;

    return (state1.songName === state2.songName &&
        state1.artistName === state2.artistName &&
        state1.albumName === state2.albumName &&
        state1.imageUrl === state2.imageUrl)
}




const CallbackPage: React.FC = () => {
    const spotifyApi = new SpotifyWebApi();
    const [spotifyToken, setSpotifyToken] = useState<string | null>(null);
    const [playbackState, setPlaybackState] = useState<PlaybackState | null>(null);
    const [mood, setMood] = useState<number[] | null>(null);
    const [color, setColor] = useState<string | null>(null);
    
    
    useEffect(() => {
        const tokens = getTokenFromUrl();
        if (tokens.access_token) {
            setSpotifyToken(tokens.access_token);
            spotifyApi.setAccessToken(tokens.access_token);

            const intervalId = setInterval(async () => {
                const newPlaybackState = await fetchPlaybackState(spotifyApi);
                if (!arePlaybackStatesEqual(playbackState, newPlaybackState)) {
                    console.log('PLAYBACK STATE CHANGED');
                    setPlaybackState(newPlaybackState);
                }
            }, 1000);

            return () => clearInterval(intervalId);
        }

    }, [spotifyToken, playbackState])


    useEffect(() => {

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