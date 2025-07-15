# Whisper API Server Usage Guide

## Overview
This server provides a REST API for OpenAI's Whisper large-v3 model for audio transcription and translation.

## Server Information
- **Model**: Whisper large-v3 
- **Device**: CUDA GPU acceleration
- **Port**: 5000
- **Max File Size**: 100MB
- **Supported Formats**: Most audio formats (wav, mp3, m4a, flac, etc.)

## API Endpoints

### 1. Health Check
```bash
curl -X GET http://YOUR_SERVER_IP:5000/health
```

### 2. Model Information
```bash
curl -X GET http://YOUR_SERVER_IP:5000/info
```

### 3. Transcribe Audio
```bash
curl -X POST \
  -F "audio=@/path/to/your/audio/file.wav" \
  http://YOUR_SERVER_IP:5000/transcribe
```

#### With optional parameters:
```bash
curl -X POST \
  -F "audio=@/path/to/your/audio/file.wav" \
  -F "language=en" \
  -F "task=transcribe" \
  http://YOUR_SERVER_IP:5000/transcribe
```

#### For translation to English:
```bash
curl -X POST \
  -F "audio=@/path/to/your/audio/file.wav" \
  -F "task=translate" \
  http://YOUR_SERVER_IP:5000/transcribe
```

## Parameters

### transcribe endpoint:
- `audio` (required): Audio file to transcribe
- `language` (optional): Language code (e.g., "en", "es", "fr"). Auto-detected if not provided
- `task` (optional): "transcribe" (default) or "translate"

## Response Format

### Health Check Response:
```json
{
  "status": "healthy",
  "model_loaded": true,
  "device": "cuda:0"
}
```

### Transcription Response:
```json
{
  "text": "The complete transcribed text",
  "language": "en",
  "task": "transcribe",
  "segments": [
    {
      "start": 0.0,
      "end": 2.5,
      "text": "First segment of speech"
    }
  ]
}
```

## Service Management

### Start the service:
```bash
sudo systemctl start whisper-api
```

### Stop the service:
```bash
sudo systemctl stop whisper-api
```

### Check service status:
```bash
sudo systemctl status whisper-api
```

### View logs:
```bash
sudo journalctl -u whisper-api -f
```

## Example Usage from Your Laptop

Replace `YOUR_SERVER_IP` with your server's IP address:

```bash
# Health check
curl -X GET http://138.197.148.238:5000/health

# Transcribe a local audio file
curl -X POST \
  -F "audio=@recording.wav" \
  http://138.197.148.238:5000/transcribe

# Transcribe with specific language
curl -X POST \
  -F "audio=@recording.wav" \
  -F "language=es" \
  http://138.197.148.238:5000/transcribe

# Translate to English
curl -X POST \
  -F "audio=@recording.wav" \
  -F "task=translate" \
  http://138.197.148.238:5000/transcribe
```

## Notes
- The server runs on all interfaces (0.0.0.0:5000)
- GPU acceleration is enabled for faster processing
- The service automatically restarts if it crashes
- Logs are available via systemd journal