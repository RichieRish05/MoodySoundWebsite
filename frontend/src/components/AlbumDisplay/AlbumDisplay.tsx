import './AlbumDisplay.css';
import { motion } from 'framer-motion';

interface AlbumDisplayProps {
    playbackState: any;
    mood: any;
    retrievalError: any;
}

const AlbumDisplay = ({ playbackState, mood, retrievalError }: AlbumDisplayProps) => {

    const MoodNames = new Map([
        ['mood_acoustic', 'Acoustic'],
        ['mood_sad', 'Sad'],
        ['mood_electronic', 'Electric'],
        ['mood_relaxed', 'Relaxed'],
        ['mood_happy', 'Happy'],
        ['danceable', 'Danceable'],
        ['mood_party', 'Party'],
        ['mood_aggressive', 'Aggressive']
    ]);

    return (
        <motion.div
            className="album-section"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -20 }}
            transition={{ duration: 0.4 }}
        >
            <div>
                {mood && <h2>Mood: {mood.map(m => MoodNames.get(m)).join(', ')}</h2>}
                {retrievalError && <h1>Could Not Fetch Song Preview</h1>}
                <img className="album-cover mb-3" src={playbackState.imageUrl} alt="album cover" />
                <h2>{playbackState.songName}</h2>
                <h3>{playbackState.artistName}</h3>
                <h4>{playbackState.albumName}</h4>
            </div>
        </motion.div>
    );
};

export default AlbumDisplay;
