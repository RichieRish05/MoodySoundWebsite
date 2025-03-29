import './HomePage.css';


const HomePage = () => {
  const clientId = import.meta.env.VITE_SPOTIFY_CLIENT_ID;
  const redirectUri = import.meta.env.VITE_SPOTIFY_REDIRECT_URI;
  const scopes = 'user-read-currently-playing user-read-playback-state';

  const handleLogin = () => {
    console.log(clientId, redirectUri, scopes);

    const authUrl = `https://accounts.spotify.com/authorize?client_id=${clientId}&redirect_uri=${encodeURIComponent(
      redirectUri
    )}&scope=${encodeURIComponent(scopes)}&response_type=token&show_dialog=true`;
    window.location.href = authUrl;
  };

  return (
    <div className="home-page-wrapper">
     <div className="main-box">
       <div className="audio-wave">
         <span></span>
         <span></span>
         <span></span>
         <span></span>
         <span></span>
       </div>


       <div className="box-content">
         <h1 className="box-title">Welcome to MoodySound AI</h1>
         <p className="subtitle">Bringing Connection Through AI</p>


         <div
           onClick={handleLogin}
           className="spotify-button"
           role="button"
           tabIndex={0}
           onKeyDown={(e) => e.key === 'Enter' && handleLogin()}
         >
           <img
             src="/spotify-logo.png"
             alt="Spotify Logo"
             className="spotify-logo"
           />
          Login with Spotify
         </div>
       </div>
     </div>
   </div>
 );
};




export default HomePage;




