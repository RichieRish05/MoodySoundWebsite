import './AlbumDisplay.css'

interface AlbumDisplayProps {
  playbackState: any;
  mood: any;
  retrievalError: any;
}

const AlbumDisplay = ({playbackState, mood, retrievalError}) => {

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
        <div className="album-section">

            <div>
                {mood && <h2>Mood: {mood.map(m => MoodNames.get(m)).join(', ')}</h2>}
                {retrievalError && <h1>Could Not Fetch Song Preview</h1>}
                <img className="album-cover mb-3" src={playbackState.imageUrl} alt="album cover" />
                <h2>{playbackState.songName}</h2>
                <h3>{playbackState.artistName}</h3>
                <h4>{playbackState.albumName}</h4>
            </div>

        </div>
    )

}

export default AlbumDisplay;