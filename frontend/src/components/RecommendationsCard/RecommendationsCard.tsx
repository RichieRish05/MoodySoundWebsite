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
  const [imageLoaded, setImageLoaded] = useState(false);
  const [imageStyle, setImageStyle] = useState<string>(showButtons ? 
    'reccomended-song-cover-w-buttons' : 'reccomended-song-cover-no-buttons')

  const onYes = (event: React.MouseEvent) => {
    setButtonsVisible(false);
    setImageStyle('reccomended-song-cover-no-buttons')
  };

  const onNo = (event: React.MouseEvent) => {
    setButtonsVisible(false);
    hideRankingBoard(true);
    setImageStyle('reccomended-song-cover-no-buttons')
  };

  return (
    <div className="card sticky-left">
      {/* Title of card */}
      <h3 className="card-title" style={{color: 'black'}}>Reccomended Song</h3>
      {/* Container for card body */}
      {recSong ? 
      <>
          <a href={recSong?.url} target="_blank" rel="noopener noreferrer" className="d-flex justify-content-center align-items-center w-100">
            {!imageLoaded && (
              <div className="image-placeholder" style={{ visibility: imageLoaded ? 'hidden' : 'visible' }}>
                Loading...
              </div>
            )}
            <img 
              src={recSong?.albumCover} 
              className={`${imageStyle} mb-2`}
              alt="Album Cover"
              style={{ display: imageLoaded ? 'block' : 'none' }}
              onLoad={() => setImageLoaded(true)}
              onError={() => setImageLoaded(true)}
            />
          </a>
          <h4>{recSong?.title}</h4> 
      </>
      : ''}
      {buttonsVisible ? (
        <div className="card-body d-flex flex-column">
          <h5>Did We Get The Mood Right?</h5>
          <button onClick={onYes} className={`reccomendation-button ${!buttonsVisible ? 'hidden' : ''}`}>Yes</button>
          <button onClick={onNo} className={`reccomendation-button ${!buttonsVisible ? 'hidden' : ''}`}>No</button>
        </div>
      ) : 
      <h1>Keep Jamming!</h1>}
    </div>
  );
};

export default RecommendationsCard; 