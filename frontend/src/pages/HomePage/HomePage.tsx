import './HomePage.css';
import Starfield from '../../components/starfield';


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
    <div className="home-page-wrapper d-flex flex-column align-items-center justify-content-center">
      <h1 className="shimmer-text text-center fixed-top mt-5">Welcome to Moodify</h1>

      <div onClick={handleLogin} className="spotify-button" style={{position: 'relative', zIndex: 1}} >
        <img src="/spotify-logo.png" alt="Spotify Logo" className="spotify-logo" />
        Login with Spotify
      </div>

      <Starfield />
    </div>


  );
};

export default HomePage;




