import DraggableMood from "../DraggableMood/draggableMood";
import MoodDropBox from "../MoodDropBox/MoodDropBox";
import React, { useEffect, useState } from 'react';
import './RankingBoard.css'
import axios from "axios";

interface RankingBoardProps {
    moods: string[];
    numPlaces: number;
    hideRankingBoard: (arg: boolean) => void;
    toggleButtons: (arg: boolean) => void;
    songInfo: Object;
}

const RankingBoard: React.FC<RankingBoardProps> = ({ moods, numPlaces, hideRankingBoard, toggleButtons, songInfo}) => {
    const [availableMoods, setAvailableMoods] = useState(moods)
    const [droppedMoods, setDroppedMoods] = useState<Record<number, string | null>>(() => {
        const initialMoods: Record<number, string | null> = {};
        for (let i = 1; i <= numPlaces; i++) {
            initialMoods[i] = null;
        }
        return initialMoods;
    });
    const [resetKey, setResetKey] = useState<number>(0)

    const onMoodDrop = (moodNumber: number, mood: string) => {
        console.log(moodNumber, mood)
        setDroppedMoods(prev => ({
            ...prev,
            [moodNumber]: mood
        }));
    }

    const onMoodCancel = (moodNumber: number) => {
        console.log(moodNumber)
        setDroppedMoods(prev => ({
            ...prev,
            [moodNumber]: null
        }));
    }

    const handleClick = (event: React.MouseEvent) => {
        event.preventDefault()
        console.log('ACCESSED')
        console.log(droppedMoods)
        setDroppedMoods(() => {
            const initialMoods: Record<number, string | null> = {};
            for (let i = 1; i <= numPlaces; i++) {
                initialMoods[i] = null;
            }
            return initialMoods;
        });

        setAvailableMoods(moods);
        setResetKey(prev => prev + 1)

        console.log('hiding board')
        hideRankingBoard(false)
        toggleButtons(false)

        const config = {
            moods: droppedMoods,
            songInfo: songInfo.songName,
            vector: songInfo.vector
        };

        axios.post(import.meta.env.VITE_BACKEND_URL + '/correctmood', config)
            .then(response => {
                console.log(response.data);
            })
            .catch(error => {
                console.error('Error details:', error.response || error);
            });
    }

    useEffect(() => {
        setAvailableMoods(moods.filter(m => !Object.values(droppedMoods).includes(m)));
    }, [droppedMoods])

    return (
        <div className={`justify-content-center d-flex flex-column align-items-center`}>
            <div className='ranking-board'>
                {Array.from({length: numPlaces}, (_, i) => i + 1).map((val) => (
                    <MoodDropBox 
                        key={`${val}-${resetKey}`}
                        moodNumber={val} 
                        onMoodDrop={onMoodDrop} 
                        onMoodCancel={onMoodCancel}
                    />
                ))}
            </div>
            
            <div className='d-flex mood-container' style={{ width: '85%', flexWrap: 'wrap', justifyContent: 'center' }}>
                {moods.map((mood) => (
                    <div key={mood} className={availableMoods.includes(mood) ? '' : 'hidden'}>
                        {mood && <DraggableMood moodLabel={mood}/>}
                    </div>
                ))}
            </div>
            
            <div className="d-flex justify-content-center pt-4">
                <button className="button" role="button" onClick={handleClick}>Submit</button>
            </div>
        </div>
    );
};

export default RankingBoard;
