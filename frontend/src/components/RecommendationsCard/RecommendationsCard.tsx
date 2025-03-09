import React, { useState } from 'react';
import './RecommendationsCard.css'
interface RecommendationsCardProps {
  makeRankingVisible: () => void;
}

const RecommendationsCard: React.FC<RecommendationsCardProps> = ({makeRankingVisible}) => {

  const [buttonsVisible, setButtonsVisible] = useState(true)


  const onYes = (event) => {
    setButtonsVisible(false)
    
  }

  const onNo = (event) => {
    setButtonsVisible(false)
    makeRankingVisible()
    console.log('ACCESSED')
    
  }


  return (
    <div className="card sticky-left">
      {/* Title of card */}
      <h5 className="card-title" style={{color: 'black'}}>Songs with Similar Moods</h5>
      {/* Container for card body */}
      <div className="card-body d-flex flex-column">
        <h5>Did We Get The Mood Right?</h5>
        <button onClick={onYes} className={`${!buttonsVisible ? 'hidden' : ''}`}>Yes</button>
        <button onClick={onNo} className={`${!buttonsVisible ? 'hidden' : ''}`}>No</button>
      </div>
    </div>
  );
};

export default RecommendationsCard; 