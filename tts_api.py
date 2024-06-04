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

app = Flask(__name__)

# load configs
config_path = "/home/ubuntu/codekijiji.ai/TTS/tts/models/xtts_config.json"
audio_config_path = "/home/ubuntu/codekijiji.ai/TTS/tts/models/xtts_config.json"

# load the audio processor
audio_config = load_config(audio_config_path)
audio_config.pop('output_path', None)  # Remove the 'output_path' key if it exists
AP = AudioProcessor(**audio_config)

# init tts model
config = GlowTTSConfig()
config.load_json(file_name=config_path)
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
