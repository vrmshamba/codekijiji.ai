import json
from TTS.tts.configs.glow_tts_config import GlowTTSConfig
from TTS.utils.audio.processor import AudioProcessor
from TTS.utils.synthesizer import synthesis
from TTS.config import load_config
from coqpit import Coqpit
from flask import Flask, request, jsonify
import os
import torch
import io
from flask import send_file
from TTS.tts.models.glow_tts import GlowTTS  # Added import statement for GlowTTS

app = Flask(__name__)

# load configs
config_path = "/home/ubuntu/codekijiji.ai/TTS/tts/models/xtts_config.json"
audio_config_path = "/home/ubuntu/codekijiji.ai/TTS/tts/models/xtts_config.json"

# load the audio processor
audio_config = load_config(audio_config_path)
audio_config = audio_config.audio  # Ensure we are accessing the 'audio' dictionary

# Debug print statements to check the structure of audio_config
print("Loaded audio_config:", audio_config)

# Ensure frame_length_ms and frame_shift_ms are set correctly
frame_length_ms = audio_config.get('frame_length_ms', 50)
frame_shift_ms = audio_config.get('frame_shift_ms', 10)
audio_config['frame_length_ms'] = frame_length_ms
audio_config['frame_shift_ms'] = frame_shift_ms

# Ensure win_length is not larger than fft_size
win_length = audio_config.get('win_length', 1024)
fft_size = audio_config.get('fft_size', 2048)
if win_length > fft_size:
    win_length = fft_size
audio_config['win_length'] = win_length
audio_config['fft_size'] = fft_size

# Ensure num_mels is set to a valid integer
num_mels = audio_config.get('num_mels', 80)
audio_config['num_mels'] = num_mels

# Debug print statements to check the values of frame_length_ms, frame_shift_ms, win_length, fft_size, and num_mels
print("frame_length_ms:", frame_length_ms)
print("frame_shift_ms:", frame_shift_ms)
print("win_length:", win_length)
print("fft_size:", fft_size)
print("num_mels:", num_mels)

# Remove 'output_path' key if it exists to avoid conflicts
audio_config.pop('output_path', None)

# Ensure audio_config is a dictionary
audio_config_dict = {key: value for key, value in audio_config.items()}

# Debug print statement to check the structure of audio_config_dict
print("audio_config_dict:", audio_config_dict)

# Ensure frame_length_ms, frame_shift_ms, win_length, fft_size, and num_mels are correctly set in the audio_config_dict
audio_config_dict['frame_length_ms'] = frame_length_ms
audio_config_dict['frame_shift_ms'] = frame_shift_ms
audio_config_dict['win_length'] = win_length
audio_config_dict['fft_size'] = fft_size
audio_config_dict['num_mels'] = num_mels

AP = AudioProcessor(**audio_config_dict)

# init tts model
config = GlowTTSConfig()
config.load_json(file_name=config_path)

# Ensure num_chars and hidden_channels are set correctly
num_chars = int(config.get('num_chars', 255))  # Set to the value from xtts_config.json
hidden_channels = int(config.get('hidden_channels', 1024))  # Set to the value from xtts_config.json
config.num_chars = num_chars
config.hidden_channels = hidden_channels

model = GlowTTS(config)
model.eval()

if torch.cuda.is_available():
    model.cuda()
    torch.set_default_tensor_type("torch.cuda.FloatTensor")

model_path = "/home/ubuntu/codekijiji.ai/TTS/tts/models/xtts_model.pth.tar"
cp = torch.load(model_path, map_location=torch.device("cpu"))
model.load_state_dict(cp["model"])
model.eval()

if torch.cuda.is_available():
    model.cuda()
    torch.set_default_tensor_type("torch.cuda.FloatTensor")

@app.route("/api/tts", methods=["POST"])
def tts():
    text = request.form["text"]
    use_cuda = False

    if torch.cuda.is_available():
        use_cuda = True

    waveform, alignment, mel_spec, mel_postnet_spec, stop_tokens, inputs = synthesis(
        model, text, "en", use_cuda, AP
    )
    out = io.BytesIO()
    save_wav(waveform, out)
    out.seek(0)
    return send_file(
        out, mimetype="audio/wav", as_attachment=True, attachment_filename="audio.wav"
    )

if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=5000)
