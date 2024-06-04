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
from TTS.tts.models.glow_tts import GlowTTS

app = Flask(__name__)

# load configs
config_path = "/home/ubuntu/codekijiji.ai/TTS/tts/models/xtts_config.json"
audio_config_path = "/home/ubuntu/codekijiji.ai/TTS/tts/models/xtts_config.json"

# load the audio config
audio_config = load_config(audio_config_path)
audio_config = audio_config.audio

# Debug print statements to check the type of audio_config
print("Type of audio_config before setting defaults:", type(audio_config))

# Ensure frame_length_ms and frame_shift_ms are not None
if audio_config.get("frame_length_ms") is None:
    audio_config["frame_length_ms"] = 50
if audio_config.get("frame_shift_ms") is None:
    audio_config["frame_shift_ms"] = 10

# Ensure win_length and fft_size are correctly set
if audio_config.get("win_length") is None or audio_config["win_length"] > audio_config.get("fft_size", 2048):
    audio_config["win_length"] = 1024
if audio_config.get("fft_size") is None:
    audio_config["fft_size"] = 2048

# Debug print statements to check the type of audio_config after setting defaults
print("Type of audio_config after setting defaults:", type(audio_config))

# Convert audio_config to dictionary
audio_config_dict = audio_config.to_dict()

# Debug print statements
print("Loaded audio_config:", audio_config_dict)
print("frame_length_ms:", audio_config_dict.get("frame_length_ms"))
print("frame_shift_ms:", audio_config_dict.get("frame_shift_ms"))
print("win_length:", audio_config_dict.get("win_length"))
print("fft_size:", audio_config_dict.get("fft_size"))

# Additional debug print statements
print("Before AudioProcessor instantiation:")
print("audio_config_dict:", audio_config_dict)

# Ensure frame_length_ms and frame_shift_ms are correctly set
audio_config_dict["frame_length_ms"] = audio_config_dict.get("frame_length_ms", 50)
audio_config_dict["frame_shift_ms"] = audio_config_dict.get("frame_shift_ms", 10)
audio_config_dict["win_length"] = audio_config_dict.get("win_length", 1024)
audio_config_dict["fft_size"] = audio_config_dict.get("fft_size", 2048)

# instantiate the audio processor
AP = AudioProcessor(**audio_config_dict)

# load the model config
config = GlowTTSConfig()
config_dict = json.load(open(config_path, "r"))
config.load_json(config_dict["model_args"])

# ensure config is not None and set num_chars and hidden_channels correctly
if config:
    num_chars = int(config.num_chars) if config.num_chars is not None else 255
    hidden_channels = int(config.hidden_channels) if config.hidden_channels is not None else 1024
    config.num_chars = num_chars
    config.hidden_channels = hidden_channels
else:
    raise ValueError("Failed to load configuration from xtts_config.json")

# load the model
model = GlowTTS(config)
model_path = "/home/ubuntu/codekijiji.ai/TTS/tts/models/speakers_xtts.pth"
cp = torch.load(model_path, map_location=torch.device("cpu"))
model.load_state_dict(cp["model"])

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
