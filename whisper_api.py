#!/usr/bin/env python3

import os
import tempfile
import whisper
import torch
from flask import Flask, request, jsonify
import logging
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # 100MB max file size

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global model variable
model = None

def load_whisper_model():
    """Load the Whisper model with appropriate device selection"""
    global model
    try:
        # Check if CUDA is available and has enough memory
        if torch.cuda.is_available():
            # Get GPU memory info
            gpu_memory = torch.cuda.get_device_properties(0).total_memory
            allocated_memory = torch.cuda.memory_allocated(0)
            available_memory = gpu_memory - allocated_memory
            
            # Large-v3 model needs about 4GB GPU memory
            if available_memory > 4 * 1024**3:  # 4GB
                device = "cuda"
                logger.info(f"Using CUDA device with {available_memory / 1024**3:.2f}GB available memory")
            else:
                device = "cpu"
                logger.info(f"Using CPU device - insufficient GPU memory ({available_memory / 1024**3:.2f}GB available)")
        else:
            device = "cpu"
            logger.info("Using CPU device - CUDA not available")
        
        model = whisper.load_model("large-v3", device=device)
        logger.info(f"Whisper large-v3 model loaded successfully on {device}")
        return True
    except Exception as e:
        logger.error(f"Failed to load Whisper model: {e}")
        return False

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'model_loaded': model is not None,
        'device': str(model.device) if model else 'none'
    })

@app.route('/transcribe', methods=['POST'])
def transcribe_audio():
    """Transcribe audio file"""
    if model is None:
        return jsonify({'error': 'Model not loaded'}), 500
    
    if 'audio' not in request.files:
        return jsonify({'error': 'No audio file provided'}), 400
    
    file = request.files['audio']
    if file.filename == '':
        return jsonify({'error': 'No audio file selected'}), 400
    
    # Get optional parameters
    language = request.form.get('language', None)
    task = request.form.get('task', 'transcribe')  # transcribe or translate
    
    try:
        # Save uploaded file to temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(file.filename)[1]) as tmp_file:
            file.save(tmp_file.name)
            temp_path = tmp_file.name
        
        # Transcribe the audio
        logger.info(f"Transcribing audio file: {file.filename}")
        result = model.transcribe(
            temp_path,
            language=language,
            task=task,
            fp16=torch.cuda.is_available()
        )
        
        # Clean up temporary file
        os.unlink(temp_path)
        
        # Return the result
        return jsonify({
            'text': result['text'],
            'language': result['language'],
            'segments': result['segments'],
            'task': task
        })
    
    except Exception as e:
        # Clean up temporary file if it exists
        if 'temp_path' in locals():
            try:
                os.unlink(temp_path)
            except:
                pass
        
        logger.error(f"Transcription error: {e}")
        return jsonify({'error': f'Transcription failed: {str(e)}'}), 500

@app.route('/info', methods=['GET'])
def model_info():
    """Get model information"""
    if model is None:
        return jsonify({'error': 'Model not loaded'}), 500
    
    return jsonify({
        'model': 'large-v3',
        'device': str(model.device),
        'supported_languages': whisper.tokenizer.LANGUAGES,
        'max_file_size': '100MB'
    })

if __name__ == '__main__':
    # Load the model on startup
    logger.info("Starting Whisper API server...")
    if not load_whisper_model():
        logger.error("Failed to load model. Exiting.")
        exit(1)
    
    # Start the Flask server
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=False,
        threaded=True
    )