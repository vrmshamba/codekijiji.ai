import os
import csv
import json
import torch
from torch.utils.data import DataLoader
from TTS.tts.configs.glow_tts_config import GlowTTSConfig
from TTS.tts.models.glow_tts import GlowTTS
from TTS.utils.audio import AudioProcessor
from TTS.tts.datasets.dataset import TTSDataset
from TTS.tts.utils.text.tokenizer import TTSTokenizer
from TTS.config import load_config
from TTS.tts.utils.text.characters import BaseCharacters

def custom_formatter(file_path, text, dataset_path, **kwargs):
    # Assuming the metadata file has the format: 'filename.wav|transcript|'
    # and the audio files are located in the dataset_path directory.
    # The file_path and text are now directly provided as arguments to the function.
    if not file_path or not text:
        # Log an error if file_path or text is missing and return an empty list
        error_message = f'Error in custom_formatter: file_path or text is missing for line: {file_path}|{text}'
        print(error_message)
        return []
    # Construct the full file path
    file_path = os.path.join(dataset_path, file_path.strip())
    # Construct the dictionary to be returned
    formatted_dict = {'audio_file': file_path, 'text': text.strip(), 'speaker_name': 'default', 'root_path': dataset_path}
    # Debug: Log the constructed dictionary before returning
    print(f'Debug: Returning from custom_formatter: {formatted_dict}')
    return [formatted_dict]

def load_tts_samples(config, eval_split=False, eval_split_size=0.2):
    items = config['items']
    if eval_split:
        split_idx = int(len(items) * (1 - eval_split_size))
        train_samples = items[:split_idx]
        eval_samples = items[split_idx:]
        return train_samples, eval_samples
    return items, []

# Define the dataset path
dataset_path = '/home/ubuntu/codekijiji.ai/data'

# Read the metadata.csv file and populate the items variable
items = []
with open(os.path.join(dataset_path, 'metadata.csv'), 'r') as csvfile:
    reader = csv.reader(csvfile, delimiter='|')
    for row in reader:
        if len(row) >= 2 and row[0].endswith('.wav'):
            file_path, text = row[0], row[1]
            items.extend(custom_formatter(file_path, text, dataset_path))

# Debug: Print the contents of the items list
print(f'Debug: Contents of items list: {items}')

# Update the formatter key to use the string name of the custom_formatter function
train_samples, eval_samples = load_tts_samples({
    'items': items,
    'formatter': 'custom_formatter',  # Pass the string name of the custom_formatter function
    'dataset_name': 'kikuyu_dataset',
    'path': dataset_path,
    'meta_file_train': 'metadata.csv',
    'meta_file_val': 'metadata.csv',
    'ignored_speakers': [],
    'language': 'kik',
    'dataset_path': dataset_path,  # Ensure dataset_path is included in the dictionary
    'meta_file_attn_mask': None  # Add the meta_file_attn_mask key with a default value
}, eval_split=True, eval_split_size=0.2)

# Paths
config_path = "/home/ubuntu/codekijiji.ai/TTS/tts/models/xtts_config.json"
model_path = "/home/ubuntu/codekijiji.ai/TTS/tts/models/xtts_model.pth.tar"
audio_config_path = "/home/ubuntu/codekijiji.ai/TTS/tts/models/xtts_config.json"

# Load configuration
config = load_config(config_path)

# Ensure characters attribute is set
if not hasattr(config, 'characters') or config.characters is None:
    config.characters = BaseCharacters(list("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!\"'(),-.:;? "), pad="_")
else:
    config.characters = BaseCharacters(config.characters.characters, pad=config.characters.pad)
print(f"Debug: Characters attribute before initializing BaseCharacters: {config.characters}")

# Ensure the characters attribute is correctly set before initializing Tokenizer
if not hasattr(config.characters, 'pad') or config.characters.pad is None:
    config.characters.pad = "_"
print(f"Debug: Characters attribute before initializing Tokenizer: {config.characters}")

# Initialize Tokenizer with explicit characters attribute
tokenizer = TTSTokenizer(characters=config.characters)

# Ensure frame_length_ms and frame_shift_ms are set
if 'audio' not in config:
    config.audio = {}
config.audio["frame_length_ms"] = config.audio.get("frame_length_ms", 50)  # Set default value to 50 ms if not present
config.audio["frame_shift_ms"] = config.audio.get("frame_shift_ms", 12.5)  # Set default value to 12.5 ms if not present

# Ensure fft_size is set
config.audio["fft_size"] = config.audio.get("fft_size", 1024)  # Set default value to 1024 if not present

# Ensure num_mels is set
config.audio["num_mels"] = config.audio.get("num_mels", 80)  # Set default value to 80 if not present

# Additional safeguard to confirm fft_size is set
if "fft_size" not in config.audio:
    config.audio["fft_size"] = 1024

# Debug: Print the fft_size value to confirm it is set correctly
print(f"Debug: fft_size = {config.audio['fft_size']}")

# Ensure frame_length_ms is set correctly to avoid win_length exceeding fft_size
max_frame_length_ms = (config.audio["fft_size"] / config.audio["sample_rate"]) * 1000
if config.audio["frame_length_ms"] > max_frame_length_ms:
    config.audio["frame_length_ms"] = max_frame_length_ms
config.audio["win_length"] = config.audio.get("win_length", 1024)  # Set default value to 1024 if not present
config.audio["fft_size"] = config.audio.get("fft_size", 1024)  # Set default value to 1024 if not present

# Ensure win_length is not larger than fft_size
if config.audio["win_length"] > config.audio["fft_size"]:
    config.audio["win_length"] = config.audio["fft_size"]
print(f"Debug: After adjustment - win_length = {config.audio['win_length']}, fft_size = {config.audio['fft_size']}")

# Debug: Print the values to confirm they are set correctly
print(f"Debug: frame_length_ms = {config.audio['frame_length_ms']}, frame_shift_ms = {config.audio['frame_shift_ms']}, win_length = {config.audio['win_length']}, fft_size = {config.audio['fft_size']}")

# Ensure the values are not None before initializing AudioProcessor
if config.audio["frame_length_ms"] is None:
    config.audio["frame_length_ms"] = 50  # Set default value to 50 ms if None
if config.audio["frame_shift_ms"] is None:
    config.audio["frame_shift_ms"] = 12.5  # Set default value to 12.5 ms if None

# Debug: Print the config.audio dictionary to verify its structure
print(f"Debug: config.audio dictionary before initializing AudioProcessor: {config.audio}")

# Additional debug print statements to confirm values
print(f"Debug: frame_length_ms = {config.audio['frame_length_ms']}, frame_shift_ms = {config.audio['frame_shift_ms']}")

# Initialize AudioProcessor
ap = AudioProcessor.init_from_config({
    "sample_rate": config.audio.get("sample_rate", 22050),
    "output_sample_rate": config.audio.get("output_sample_rate", 24000),
    "frame_length_ms": config.audio["frame_length_ms"],
    "frame_shift_ms": config.audio["frame_shift_ms"],
    "win_length": config.audio["win_length"],
    "fft_size": config.audio["fft_size"],
    "num_mels": config.audio["num_mels"]
})

# Ensure characters attribute is set before initializing Tokenizer
if not hasattr(config, 'characters') or config.characters is None:
    config.characters = BaseCharacters(list("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!\"'(),-.:;? "), pad="_")
# Debug: Print the characters attribute to verify it is set correctly
print(f"Debug: Characters attribute before initializing Tokenizer: {config.characters}")

# Initialize Tokenizer with explicit characters attribute
tokenizer = TTSTokenizer(config.characters)

# Prepare Dataset
dataset = TTSDataset(
    dataset_path,
    config,
    ap,
    tokenizer,
    speaker_id=None,
    use_noise_augment=config.use_noise_augment,
)

# Prepare DataLoader
dataloader = DataLoader(
    dataset,
    batch_size=config.batch_size,
    shuffle=True,
    num_workers=4,
    pin_memory=True,
)

# Initialize model
model = GlowTTS(config)

# Define optimizer and loss function
optimizer = torch.optim.Adam(model.parameters(), lr=config.lr)
criterion = torch.nn.MSELoss()

# Training loop
num_epochs = config.epochs
for epoch in range(num_epochs):
    model.train()
    for batch in dataloader:
        optimizer.zero_grad()
        text, mel, speaker_ids = batch
        text, mel = text.to(model.device), mel.to(model.device)
        outputs = model(text, mel)
        loss = criterion(outputs, mel)
        loss.backward()
        optimizer.step()

# Save model
torch.save(model.state_dict(), model_path)
print(f"Model saved to {model_path}")
