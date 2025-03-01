



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
    <button onClick={handleLogin}>
      Login with Spotify
    </button>
  );
};

export default HomePage;




