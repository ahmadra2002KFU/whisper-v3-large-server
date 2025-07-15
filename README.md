# Whisper v3 Large Server

A high-performance REST API server for OpenAI's Whisper large-v3 model, designed for audio transcription and translation with GPU acceleration.

## Features

- 🚀 **GPU Accelerated**: Optimized for CUDA-enabled GPUs
- 🌍 **100+ Languages**: Supports transcription and translation for 100+ languages
- 🔄 **Auto-detection**: Automatically detects audio language
- 📡 **REST API**: Simple HTTP endpoints for easy integration
- 🔄 **Translation**: Translate any language to English
- 📦 **Large Files**: Supports up to 100MB audio files
- 🛠️ **Production Ready**: Includes systemd service configuration
- 📝 **Comprehensive Logging**: Full request and error logging

## Quick Start

### Prerequisites

- Python 3.8+
- CUDA-compatible GPU (recommended)
- PyTorch with CUDA support
- 4GB+ GPU memory for optimal performance

### Installation

1. Clone the repository:
```bash
git clone https://github.com/YOUR_USERNAME/whisper-v3-large-server.git
cd whisper-v3-large-server
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Start the server:
```bash
python whisper_api.py
```

The server will start on `http://0.0.0.0:5000`

## API Endpoints

### Health Check
```bash
curl -X GET http://localhost:5000/health
```

**Response:**
```json
{
  "status": "healthy",
  "model_loaded": true,
  "device": "cuda:0"
}
```

### Model Information
```bash
curl -X GET http://localhost:5000/info
```

**Response:**
```json
{
  "model": "large-v3",
  "device": "cuda:0",
  "supported_languages": {...},
  "max_file_size": "100MB"
}
```

### Transcribe Audio
```bash
curl -X POST \
  -F "audio=@your_audio_file.wav" \
  http://localhost:5000/transcribe
```

**With optional parameters:**
```bash
curl -X POST \
  -F "audio=@your_audio_file.wav" \
  -F "language=en" \
  -F "task=transcribe" \
  http://localhost:5000/transcribe
```

**For translation to English:**
```bash
curl -X POST \
  -F "audio=@your_audio_file.wav" \
  -F "task=translate" \
  http://localhost:5000/transcribe
```

**Response:**
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

## Parameters

### `/transcribe` endpoint:
- `audio` (required): Audio file to transcribe
- `language` (optional): Language code (e.g., "en", "es", "fr"). Auto-detected if not provided
- `task` (optional): "transcribe" (default) or "translate"

## Supported Audio Formats

- WAV
- MP3
- M4A
- FLAC
- OGG
- And many more formats supported by FFmpeg

## Production Deployment

### Using systemd (Linux)

1. Copy the service file:
```bash
sudo cp whisper-api.service /etc/systemd/system/
```

2. Update the service file paths to match your installation directory

3. Enable and start the service:
```bash
sudo systemctl daemon-reload
sudo systemctl enable whisper-api
sudo systemctl start whisper-api
```

4. Check service status:
```bash
sudo systemctl status whisper-api
```

5. View logs:
```bash
sudo journalctl -u whisper-api -f
```

### Using Docker (Optional)

```dockerfile
FROM python:3.10-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY whisper_api.py .
EXPOSE 5000

CMD ["python", "whisper_api.py"]
```

## Configuration

The server can be configured through environment variables:

- `CUDA_VISIBLE_DEVICES`: Specify which GPU to use (default: 0)
- `FLASK_HOST`: Host to bind to (default: 0.0.0.0)
- `FLASK_PORT`: Port to bind to (default: 5000)

## Performance

### GPU Memory Usage
- **Whisper large-v3**: ~4GB GPU memory
- **Inference**: Additional ~1-2GB during processing
- **Recommended**: 6GB+ GPU memory for optimal performance

### Processing Speed
- **GPU (RTX 6000)**: ~0.1x real-time (10 minutes audio in ~1 minute)
- **CPU**: ~2-5x real-time (10 minutes audio in ~20-50 minutes)

## Error Handling

The API returns appropriate HTTP status codes:

- `200`: Success
- `400`: Bad request (missing audio file, invalid parameters)
- `500`: Server error (model loading failed, transcription error)

Error responses include detailed error messages:
```json
{
  "error": "No audio file provided"
}
```

## Logging

The server provides comprehensive logging:

- Request logging via Flask/Werkzeug
- Model loading and initialization
- Transcription processing status
- Error details for debugging

## Security Considerations

- File size limits (100MB default)
- Temporary file cleanup
- Input validation
- Consider adding authentication for production use

## Troubleshooting

### Common Issues

1. **CUDA Out of Memory**
   - Reduce batch size or use CPU mode
   - Check GPU memory usage with `nvidia-smi`

2. **Model Loading Errors**
   - Ensure sufficient disk space (~3GB for model)
   - Check internet connection for initial download

3. **Audio File Issues**
   - Verify file format is supported
   - Check file isn't corrupted
   - Ensure file size is under 100MB

### Performance Optimization

1. **GPU Usage**
   - Ensure CUDA is properly installed
   - Use appropriate PyTorch version for your CUDA version
   - Monitor GPU utilization with `nvidia-smi`

2. **Memory Management**
   - Close unused applications to free GPU memory
   - Use appropriate batch sizes for your GPU

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- OpenAI for the Whisper model
- PyTorch team for the deep learning framework
- Flask team for the web framework

## Support

For issues and questions:
- Open an issue on GitHub
- Check the troubleshooting section
- Review the logs for error details