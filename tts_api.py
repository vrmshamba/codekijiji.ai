from flask import Flask, request, jsonify, send_file
import os
import torch
import base64
from io import BytesIO
from tts.models import GlowTTS
from tts.config import GlowTTSConfig
from tts.audio import AudioProcessor

app = Flask(__name__)

# Load the trained TTS model
model_path = "/home/ec2-user/codekijiji.ai/models/kikuyu_glow_tts/model.pth"
config_path = "/home/ec2-user/codekijiji.ai/models/kikuyu_glow_tts/config.json"
audio_config_path = "/home/ec2-user/codekijiji.ai/models/kikuyu_glow_tts/audio_config.json"

model = GlowTTS.load_from_checkpoint(model_path, config_path)
audio_processor = AudioProcessor.init_from_config(audio_config_path)

@app.route('/tts', methods=['POST'])
def tts():
    data = request.get_json()
    text = data.get('text', '')

    if not text:
        return jsonify({'error': 'No text provided'}), 400

    # Generate audio from text
    audio = model.generate(text)
    audio_wav = audio_processor.save_wav(audio)

    # Convert audio to base64
    audio_buffer = BytesIO()
    audio_processor.save_wav(audio, audio_buffer)
    audio_base64 = base64.b64encode(audio_buffer.getvalue()).decode('utf-8')

    return jsonify({'audio': audio_base64})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
