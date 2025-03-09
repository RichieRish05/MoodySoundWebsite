import React, { use, useState } from 'react';
import './draggableMoods.css'

const DraggableMood = ({moodLabel}) => {

    const handleClick = (event) => {
        console.log('HEY')
    }

    const handleDrag = (event) => {
        console.log(`Drag started ${moodLabel}`)
        event.dataTransfer.setData('mood', moodLabel)
    }

    return (
        <div
        onClick={(e) => handleClick(e)}
        draggable="true"
        onDragStart={(e) => handleDrag(e)}
        className='draggable-mood m-1'

        >
            {moodLabel}
        </div>
    )

}

export default DraggableMood;