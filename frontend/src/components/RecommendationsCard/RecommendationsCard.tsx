import React from 'react';
import './RecommendationsCard.css';

// Props expected by the RecommendationsCard component
interface RecommendationsCardProps {
  hideRankingBoard: (arg: boolean) => void;  // Function to toggle the ranking board visibility
  showButtons: boolean;                      // Controls whether Yes/No buttons are shown
  onYesClick: () => void;                    // Callback when user clicks "Yes"
}

const RecommendationsCard: React.FC<RecommendationsCardProps> = ({
  hideRankingBoard,
  showButtons,
  onYesClick
}) => {

  // Called when the user agrees with the mood detection
  const onYes = (event: React.MouseEvent) => {
    onYesClick();
  };

  // Called when the user disagrees and wants to rank moods manually
  const onNo = (event: React.MouseEvent) => {
    hideRankingBoard(true);
    console.log('ACCESSED'); // Optional debug log
  };

  return (
    <div className="card sticky-left">
      {showButtons ? (
        <>
          <h5 className="card-title" style={{ color: 'black' }}>
            Songs with Similar Moods
          </h5>

          <div className="card-body d-flex flex-column">
            <h5>Did We Get The Mood Right?</h5>
            <button onClick={onYes}>Yes</button>
            <button onClick={onNo}>No</button>
          </div>
        </>
      ) : (
        <h5 className="card-title" style={{ color: 'black' }}>
          Songs with Similar Moods
        </h5>
      )}
    </div>
  );
};

export default RecommendationsCard;
