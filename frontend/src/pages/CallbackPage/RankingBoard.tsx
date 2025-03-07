import React, { useState } from "react";
import "./RankingBoard.css";

const initialItems = [
    "Happy", "Party", "Relaxed", "Sad",
    "Aggresive", "Electronic", "Danceable", "Acoustic"
];

const RankingBoard: React.FC = () => {
    const [rankedItems, setRankedItems] = useState<(string | null)[]>([null, null, null]);
    const [draggableItems, setDraggableItems] = useState<string[]>(initialItems);

    // Handles when a draggable item is picked up
    const onDragStart = (event: React.DragEvent<HTMLDivElement>, item: string) => {
        event.dataTransfer.setData("text/plain", item);
        event.dataTransfer.effectAllowed = "move";
    };

    // Handles when an item is dropped into a ranking slot
    const onDrop = (event: React.DragEvent<HTMLDivElement>, index: number) => {
        event.preventDefault();
        const item = event.dataTransfer.getData("text/plain");

        // Prevent duplicate entries in the ranking board
        if (!rankedItems.includes(item)) {
            setRankedItems(prev => {
                const newRanking = [...prev];
                newRanking[index] = item;
                return newRanking;
            });

            // Remove item from the draggable list
            setDraggableItems(prev => prev.filter(i => i !== item));
        }
    };

    // Allows items to be dragged over the drop area
    const onDragOver = (event: React.DragEvent<HTMLDivElement>) => {
        event.preventDefault();
    };

    // Handles removing a ranked item and returning it to the draggable list
    const onRemove = (index: number) => {
        if (rankedItems[index]) {
            setDraggableItems(prev => [...prev, rankedItems[index] as string]);
            setRankedItems(prev => {
                const newRanking = [...prev];
                newRanking[index] = null;
                return newRanking;
            });
        }
    };

    return (
        <div className="ranking-container">
            <h2>Ranking Board</h2>
            <div className="rank-section">
                {rankedItems.map((item, index) => (
                    <div
                        key={index}
                        className="rank-box"
                        onDrop={(event) => onDrop(event, index)}
                        onDragOver={onDragOver}
                    >
                        {item ? (
                            <span className="ranked-item" onClick={() => onRemove(index)}>
                                {item} ❌
                            </span>
                        ) : (
                            `Rank ${index + 1}`
                        )}
                    </div>
                ))}
            </div>
            <div className="draggable-items">
                {draggableItems.map((item) => (
                    <div
                        key={item}
                        className="draggable-item"
                        draggable
                        onDragStart={(event) => onDragStart(event, item)}
                    >
                        {item}
                    </div>
                ))}
            </div>
        </div>
    );
};

export default RankingBoard;
