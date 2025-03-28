# MoodySoundWebsite 🎵

MoodySoundWebsite is a web application that analyzes the mood of your currently playing Spotify songs using machine learning. It provides real-time mood analysis, color visualization, and song recommendations based on mood patterns.

## Features 🌟

- **Real-time Mood Analysis**: Analyzes the currently playing Spotify track and determines its emotional characteristics
- **Dynamic Color Visualization**: Changes background color based on the detected mood
- **Mood Correction**: Users can provide feedback on mood analysis to improve accuracy
- **Similar Song Recommendations**: Suggests songs with similar mood patterns
- **Multi-mood Detection**: Identifies multiple emotional aspects of a song
- **Interactive UI**: Drag-and-drop interface for mood ranking

## Technology Stack 🛠️

### Frontend
- React + TypeScript
- Bootstrap for styling
- Spotify Web API integration
- Axios for HTTP requests

### Backend
- Flask (Python)
- PyTorch for ML model
- Librosa for audio processing
- AWS DynamoDB for data storage
- AWS S3 for file storage



## How It Works 🎯

1. **Authentication**: 
   - Users log in with their Spotify account
2. **Song Analysis**: 
   - Captures audio from currently playing Spotify track
   - Generates spectrograms for audio analysis
   - Processes through ML model to determine mood
3. **Mood Visualization**:
   - Displays primary moods detected in the song
   - Changes background color based on mood combination
4. **User Feedback**:
   - Users can correct mood analysis
   - Feedback is used to enhance the ML model
5. **Similar Songs**:
   - Recommends songs with matching mood patterns
   - Uses DynamoDB for efficient mood-based queries

## Mood Categories 🎭

- Danceable
- Acoustic
- Aggressive
- Electronic
- Happy
- Party
- Relaxed
- Sad

## Contributing 🤝

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the project
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request


## Contact

Rishi Murumkar - [rmurumka@uci.edu]

## Acknowledgments 🙏

- Special thanks to the UCI Department of Computer Science for their support
- ZOT ZOT ZOT!


