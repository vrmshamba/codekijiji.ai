import json
from TTS.tts.configs.glow_tts_config import GlowTTSConfig

with open('/home/ubuntu/codekijiji.ai/TTS/tts/models/xtts_config.json') as f:
    config_data = json.load(f)
    config_data.pop('model_dir', None)  # Remove the 'model_dir' key if it exists
    config_data.pop('languages', None)  # Remove the 'languages' key if it exists
    config_data.pop('temperature', None)  # Remove the 'temperature' key if it exists
    # Remove any other unexpected keys
    valid_keys = GlowTTSConfig.__annotations__.keys()
    config_data = {k: v for k, v in config_data.items() if k in valid_keys}
    config = GlowTTSConfig(**config_data)
    print(config)
