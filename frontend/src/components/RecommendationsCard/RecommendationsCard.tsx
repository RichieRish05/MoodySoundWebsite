import React, { useState } from 'react';
import './RecommendationsCard.css';

interface RecommendationsCardProps {
  key: number;
  hideRankingBoard: (arg: boolean) => void;
  showButtons: boolean;
  recSong: Record<string, any>;
}

const RecommendationsCard: React.FC<RecommendationsCardProps> = ({hideRankingBoard, showButtons, recSong}) => {
  const [buttonsVisible, setButtonsVisible] = useState(showButtons);

  const onYes = (event: React.MouseEvent) => {
    setButtonsVisible(false);
  };

  const onNo = (event: React.MouseEvent) => {
    setButtonsVisible(false);
    hideRankingBoard(true);
    console.log('ACCESSED');
  };

  return (
    <div className="card sticky-left">
      {/* Title of card */}
      <h5 className="card-title" style={{color: 'black'}}>Songs with Similar Moods</h5>
      {/* Container for card body */}
      {recSong ? <h1>{recSong.title}</h1> : ''}
      {buttonsVisible && (
        <div className="card-body d-flex flex-column">
          <h5>Did We Get The Mood Right?</h5>
          <button onClick={onYes} className={!buttonsVisible ? 'hidden' : ''}>Yes</button>
          <button onClick={onNo} className={!buttonsVisible ? 'hidden' : ''}>No</button>
        </div>
      )}
    </div>
  );
};

export default RecommendationsCard; 