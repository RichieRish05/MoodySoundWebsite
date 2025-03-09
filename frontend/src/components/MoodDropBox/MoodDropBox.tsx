import React, { useState } from 'react';
import './MoodDropBox.css'

const MoodDropBox = ({moodNumber, onMoodDrop, onMoodCancel}) => {
    const [draggedOver, setDraggedOver] = useState(false);
    const [mood, setMood] = useState<string | null>(null);
    const [showButton, setShowButton] = useState<true | false>(false)

    const handleDrop = (event: React.DragEvent<HTMLDivElement>) => {
        const mood = event.dataTransfer.getData('mood') as string;
        setMood(mood)
        setShowButton(true)
        onMoodDrop(moodNumber, mood)
    }

    const handleDragOver = (event: React.DragEvent<HTMLDivElement>) => {
        event.preventDefault()
        setDraggedOver(true);
    }

    const handleClick = (event) => {
        setMood(null);
        setShowButton(false);
        onMoodCancel(moodNumber)

    }
    return (
        <div 
        className='dropbox mx-2 mb-5'
        onDrop={handleDrop}
        onDragOver={handleDragOver}
        >
            {mood ? (
                <div>
                    {mood}
                    <button 
                        onClick={handleClick}
                        className='x-button'
                    >
                        ×
                    </button>
                </div>
            ) : moodNumber}
        </div>
    )
}

export default MoodDropBox;