import { useEffect, useState } from 'react';
import SpotifyWebApi from 'spotify-web-api-js';
import axios from 'axios';
import './CallbackPage.css';
import Starfield from '../../components/starfield';

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
        state1.albumName === state2.albumName)
}




const CallbackPage: React.FC = () => {
    const spotifyApi = new SpotifyWebApi();
    const [spotifyToken, setSpotifyToken] = useState<string | null>(null);
    const [playbackState, setPlaybackState] = useState<PlaybackState | null>(null);
    const [mood, setMood] = useState<number[] | null>(null);
    const [color, setColor] = useState<string | null>("#FFFFFF");
    
    useEffect(() => {
        const tokens = getTokenFromUrl();
        if (tokens.access_token) {
            setSpotifyToken(tokens.access_token);
            spotifyApi.setAccessToken(tokens.access_token);
        }
    }, []);

    useEffect(() => {
        if (!spotifyToken) return;
    
        let lastPlaybackState = playbackState; // Keep track of the last state
    
        const updatePlaybackState = async () => {
            try {
                const currentPlaybackState = await fetchPlaybackState(spotifyApi);
                
                if (!arePlaybackStatesEqual(lastPlaybackState, currentPlaybackState)) {
                    setPlaybackState(currentPlaybackState);
                    lastPlaybackState = currentPlaybackState; // Update lastPlaybackState only if it changes
                }
            } catch (error) {
                console.error("Error fetching playback state:", error);
            }
        };
    
        updatePlaybackState(); // Fetch immediately on mount
    
        const intervalId = setInterval(updatePlaybackState, 3000); // Update the playback state every 3 seconds
    
        return () => clearInterval(intervalId);
    }, [spotifyToken]); // Only re-run when spotifyToken changes
    

    useEffect(() => {
        const fetchMood = async (songName, artistName) => {
            const mood = await axios.get(`${BACKEND_URL}/mood?song=${songName}&artist=${artistName}`)
                .then((res) => {
                    console.log(res.data);
                    return res.data;

                })
                .catch((err) => {
                    console.error(err);
                    return null;
                });

            return mood;
        }

        if (playbackState) {
            const fetchAndSetMood = async () => {
                const mood = await fetchMood(playbackState.songName, playbackState.artistName);
                if (mood) {
                    setMood(mood.significant_moods);
                    setColor(mood.color);
                }
            };
            fetchAndSetMood();
        }
    }, [playbackState])


    useEffect(() => {
        document.body.style.transition = 'background-color 0.5s ease';

        document.body.style.backgroundColor = color || "#FFFFFF";

        return () => {
            document.body.style.backgroundColor = '';
            document.body.style.transition = '';
        };
    }, [color]);





    return (
        <div className="vh-100 d-flex flex-column align-items-center justify-content-center">
            <h1>Welcome</h1>

            {mood && <h2>Mood: {mood.join(', ')}</h2>}

            {playbackState && (
                <div>
                    <img src={playbackState.imageUrl} alt="album cover" />
                    <h2>{playbackState.songName}</h2>
                    <h3>{playbackState.artistName}</h3>
                    <h4>{playbackState.albumName}</h4>
                </div>
            )}

            <Starfield />

        </div>
    )
}

export default CallbackPage;