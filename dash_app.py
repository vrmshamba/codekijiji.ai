# Import required libraries
import dash
from dash import dcc, html
import plotly.express as px
import pandas as pd
import logging
import requests
import base64
from dash.dependencies import Input, Output, State

# Initialize logging
logging.basicConfig(level=logging.INFO)

# Load and preprocess data
try:
    df = pd.read_csv('synthetic_data.csv')
except Exception as e:
    logging.error(f"Error loading data: {e}")
    raise e

# Calculate the count of submissions per language
try:
    language_counts = df['language'].value_counts().reset_index()
    language_counts.columns = ['language', 'count']
except Exception as e:
    logging.error(f"Error processing language counts: {e}")
    raise e

# Initialize the Dash app
app = dash.Dash(__name__)

# Define the app layout
app.layout = html.Div([
    html.H1("Data Visualizations for 'codekiijiji.ai'"),
    html.Div([
        html.H2("Language Distribution"),
        dcc.Graph(
            id='language-distribution',
            figure=px.bar(language_counts, x='language', y='count', title="Language Distribution")
        )
    ]),
    html.Div([
        html.H2("Submission Times vs User ID"),
        dcc.Graph(
            id='submission-times',
            figure=px.scatter(df, x='submitted_at', y='user_id', title="Submission Times vs User ID")
        )
    ]),
    # Add more visualizations as needed
    html.Div([
        html.H2("Text-to-Speech (TTS) System"),
        dcc.Input(id='tts-input', type='text', placeholder='Enter text for TTS'),
        html.Button('Submit', id='tts-submit', n_clicks=0),
        html.Audio(id='tts-audio', controls=True)
    ])
])

# Define callback functions for interactivity
@app.callback(
    Output('tts-audio', 'src'),
    Input('tts-submit', 'n_clicks'),
    State('tts-input', 'value')
)
def update_tts_audio(n_clicks, text):
    if n_clicks > 0 and text:
        response = requests.post('http://54.235.154.24:5000/tts', json={'text': text})
        if response.status_code == 200:
            audio_content = response.json().get('audio', '')
            audio_src = f"data:audio/wav;base64,{audio_content}"
            return audio_src
    return None

# Run the server
if __name__ == '__main__':
    app.run_server(debug=False, host='0.0.0.0', port=8050)
