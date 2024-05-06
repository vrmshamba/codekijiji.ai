# Import required libraries
import dash
from dash import dcc, html
import plotly.express as px
import pandas as pd
import logging

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
])

# Define callback functions for interactivity (if necessary)
# This is a placeholder for callback functions
# Add callback functions here

# Run the server
if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0', port=8050)
