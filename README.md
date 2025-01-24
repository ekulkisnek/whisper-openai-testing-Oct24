
# Audio Transcription Service

A Flask-based web application that transcribes audio files into text using OpenAI's Whisper model. This application provides a simple interface for users to upload audio files and receive text transcriptions.

## Features

- Supports multiple audio formats (WAV, MP3, OGG, FLAC, AAC, M4A, WMA, AIFF)
- Chunk-based processing for large audio files
- Real-time progress tracking
- Web-based user interface
- Automatic transcript file management

## Prerequisites

- Python 3.11+
- Flask
- OpenAI Whisper
- PyDub
- Other dependencies listed in requirements.txt

## Setup

1. Fork this project on Replit
2. The dependencies will be automatically installed
3. Click the Run button

## Usage

1. Access the web interface through your browser
2. Click "Choose File" to select an audio file
3. Click "Transcribe" to start the transcription process
4. Wait for the process to complete
5. The transcription will appear on the page and be saved in the `transcripts` folder

## Project Structure

```
├── static/
│   └── styles.css          # CSS styles for the web interface
├── templates/
│   └── index.html          # Main web interface template
├── transcripts/            # Directory for storing transcription results
├── uploads/               # Directory for temporary audio file storage
├── app.py                 # Flask application setup and routes
├── audio_processor.py     # Audio processing and transcription logic
└── main.py               # Application entry point
```

## API Endpoints

- `GET /`: Renders the main page
- `POST /upload`: Handles audio file upload and transcription

## Technical Details

- The application splits audio files into 15-second chunks for processing
- Uses Whisper's base model for transcription
- Provides real-time progress updates
- Automatically cleans up temporary files
- Supports concurrent user requests

## Limitations

- Maximum file size depends on available system memory
- Processing time varies based on audio length and system resources
- Requires active internet connection for model loading

## Contributing

To contribute:
1. Fork the project on Replit
2. Make your changes
3. Test thoroughly
4. Submit a pull request

## License

Open source and free to use.
