import { useEffect, useState } from 'react';
import SpotifyWebApi from 'spotify-web-api-js';
import axios from 'axios';
import './CallbackPage.css';
import RankingBoard from '../../components/RankingBoard/RankingBoard';
import RecommendationsCard from '../../components/RecommendationsCard/RecommendationsCard';
import AlbumDisplay from '../../components/AlbumDisplay/AlbumDisplay';
import { AnimatePresence, motion } from 'framer-motion';

const BACKEND_URL = import.meta.env.VITE_BACKEND_URL;

// Represents the current song's playback details
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

// Extract access token from the Spotify auth URL hash
const getTokenFromUrl = (): TokenResponse => {
    return window.location.hash
        .substring(1)
        .split('&')
        .reduce((initial: Record<string, string>, item) => {
            let parts = item.split('=');
            initial[parts[0]] = decodeURIComponent(parts[1]);
            return initial;
        }, {} as Record<string, string>);
};

// Converts Spotify playback data into a simplified PlaybackState
const parsePlaybackState = (playbackState: any): PlaybackState | null => {
    if (playbackState.currently_playing_type === 'track') {
        return {
            songName: playbackState.item.name,
            artistName: playbackState.item.artists.map((artist: any) => artist.name).join(', '),
            albumName: playbackState.item.album.name,
            imageUrl: playbackState.item.album.images[0].url,
        };
    }
    return null;
};

// Fetches the current playback state from Spotify's API
const fetchPlaybackState = async (spotifyApi: SpotifyWebApi.SpotifyWebApiJs): Promise<PlaybackState | null> => {
    let res = await spotifyApi.getMyCurrentPlaybackState();
    return parsePlaybackState(res);
};

// Compares two playback states to detect song changes
const arePlaybackStatesEqual = (state1: PlaybackState | null, state2: PlaybackState | null): boolean => {
    if (state1 === null && state2 === null) return true;
    if (state1 === null || state2 === null) return false;

    return (
        state1.songName === state2.songName &&
        state1.artistName === state2.artistName &&
        state1.albumName === state2.albumName
    );
};

const CallbackPage: React.FC = () => {
    const spotifyApi = new SpotifyWebApi();

    // Spotify access token
    const [spotifyToken, setSpotifyToken] = useState<string | null>(null);

    // Current song playback state
    const [playbackState, setPlaybackState] = useState<PlaybackState | null>(null);

    // Mood analysis result for the current song
    const [mood, setMood] = useState<number[] | null>(null);

    // Color representing the song's mood
    const [color, setColor] = useState<string | null>('#FFFFFF');

    // If true, there was an error retrieving mood data
    const [retrievalError, setRetrievalError] = useState<boolean>(false);

    // Controls whether the ranking board is shown
    const [displayRankingBoard, setDisplayRankingBoard] = useState<boolean>(false);

    // Controls visibility of Yes/No buttons on the recommendations card
    const [showRecButtons, setShowRecButtons] = useState<boolean>(true);

    // Get token from URL hash and set it in the Spotify API
    useEffect(() => {
        const tokens = getTokenFromUrl();
        if (tokens.access_token) {
            setSpotifyToken(tokens.access_token);
            spotifyApi.setAccessToken(tokens.access_token);
        }
    }, []);

    // Poll Spotify API every 3 seconds for playback state updates
    useEffect(() => {
        if (!spotifyToken) return;

        let lastPlaybackState = playbackState;

        const updatePlaybackState = async () => {
            try {
                const currentPlaybackState = await fetchPlaybackState(spotifyApi);

                // Only update if song changed
                if (!arePlaybackStatesEqual(lastPlaybackState, currentPlaybackState)) {
                    setPlaybackState(currentPlaybackState);
                    lastPlaybackState = currentPlaybackState;
                }
            } catch (error) {
                console.error('Error fetching playback state:', error);
            }
        };

        updatePlaybackState();

        const intervalId = setInterval(updatePlaybackState, 3000);

        return () => clearInterval(intervalId);
    }, [spotifyToken]);

    // When playback state changes, fetch mood and color for the new song
    useEffect(() => {
        const fetchMood = async (songName: string, artistName: string) => {
            try {
                const response = await axios.get(`${BACKEND_URL}/mood?song=${songName}&artist=${artistName}`);
                return response.data;
            } catch (error) {
                console.error(error);
                return null;
            }
        };

        if (playbackState) {
            const fetchAndSetMood = async () => {
                const moodData = await fetchMood(playbackState.songName, playbackState.artistName);

                if (moodData) {
                    setRetrievalError(false);
                    setMood(moodData.significant_moods);
                    setColor(moodData.color);
                } else {
                    setRetrievalError(true);
                    setMood(null);
                    setColor('#FFFFFF');
                }
            };

            fetchAndSetMood();
        }
    }, [playbackState]);

    // Reset UI components when a new song starts playing
    useEffect(() => {
        if (playbackState) {
            setShowRecButtons(true);
            setDisplayRankingBoard(false);
        }
    }, [playbackState]);

    // Updates the background color based on mood
    useEffect(() => {
        document.body.style.transition = 'background-color 0.5s ease';
        document.body.style.backgroundColor = color || '#FFFFFF';

        return () => {
            document.body.style.backgroundColor = '';
            document.body.style.transition = '';
        };
    }, [color]);

    // List of available moods for the ranking board
    const moods = [
        'Happy', 'Party', 'Relaxed', 'Sad',
        'Aggressive', 'Electronic', 'Danceable', 'Acoustic'
    ];

    // Handles the user clicking "Yes" on the recommendations card
    const handleYesClick = () => {
        setShowRecButtons(false);
    };

    return (
        <div>
            <h1 className='site-title'>MoodySoundAI</h1>

            <div className="page-content d-flex justify-content-between">
                <div>
                    <AnimatePresence mode="wait">
                        {playbackState && (
                            <motion.div
                                key={playbackState.songName} // re-renders when song changes
                                initial={{ opacity: 0, y: 20 }}
                                animate={{ opacity: 1, y: 0 }}
                                exit={{ opacity: 0, y: -20 }}
                                transition={{ duration: 0.4 }}
                            >
                                <AlbumDisplay
                                    playbackState={playbackState}
                                    retrievalError={retrievalError}
                                    mood={mood}
                                />
                            </motion.div>
                        )}
                    </AnimatePresence>
                </div>

                <div className="right-panel mt-2">
                    {playbackState && (
                        displayRankingBoard ? (
                            <RankingBoard
                                hideRankingBoard={setDisplayRankingBoard}
                                moods={moods}
                                numPlaces={3}
                                toggleButtons={setShowRecButtons}
                            />
                        ) : (
                            <RecommendationsCard
                                hideRankingBoard={setDisplayRankingBoard}
                                showButtons={showRecButtons}
                                onYesClick={handleYesClick}
                            />
                        )
                    )}
                </div>
            </div>
        </div>
    );
};

export default CallbackPage;
