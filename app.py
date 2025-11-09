# app.py - Main Dash Application
import dash
from dash import dcc, html, Input, Output, State, callback_context, dash_table
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff
import pandas as pd
import numpy as np
from datetime import datetime
import base64
import io
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
import warnings
warnings.filterwarnings('ignore')

# Load data from your cleaned repository
matches = pd.read_csv('./data/cleaned/matches.csv')
deliveries = pd.read_csv('./data/cleaned/deliveries.csv')

# Import custom modules
from utils.preprocess import preprocess_matches_data, preprocess_deliveries_data, calculate_player_stats
from utils.aggregates import calculate_team_performance, calculate_venue_stats
from ml.similarity_engine import PlayerSimilarityEngine
from ml.predict_winner import IPLWinPredictor

# Preprocess data
matches = preprocess_matches_data(matches)
deliveries = preprocess_deliveries_data(deliveries)

# Initialize Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])
app.title = "🏏 IPL Analytics Dashboard - Advanced Edition"
server = app.server

# Team colors and configuration
team_colors = {
    'Mumbai Indians': '#004BA0', 'Chennai Super Kings': '#FFFF00', 
    'Royal Challengers Bangalore': '#EC1C24', 'Kolkata Knight Riders': '#3A225D',
    'Delhi Capitals': '#2561AE', 'Punjab Kings': '#ED1B24', 
    'Rajasthan Royals': '#FF1C5B', 'Sunrisers Hyderabad': '#FF822A',
    'Gujarat Titans': '#1B2133', 'Lucknow Super Giants': '#FF6B00',
    'Deccan Chargers': '#004BA0', 'Pune Warriors': '#C0C0C0',
    'Kochi Tuskers Kerala': '#8B4513', 'Rising Pune Supergiant': '#D1005F'
}

# Initialize ML models
predictor = IPLWinPredictor()
predictor.train_model(matches, deliveries)

player_stats = calculate_player_stats(deliveries, matches)
similarity_engine = PlayerSimilarityEngine()
similarity_engine.create_player_vectors(player_stats)

# Import component modules
from components.header import create_header
from components.navigation import create_navigation
from components.season_view import create_season_tab
from components.match_view import create_match_tab
from components.player_view import create_player_tab
from components.pvp_view import create_pvp_tab
from components.pvt_view import create_pvt_tab
from components.venue_view import create_venue_tab
from components.compare_view import create_compare_tab
from components.ml_view import create_ml_tab
from components.dreamxi_view import create_dreamxi_tab
from components.records_view import create_records_tab

# Main App Layout
app.layout = html.Div([
    html.Div([
        create_header(matches),
        create_navigation(),
        
        html.Div(id="tab-content", className="tab-content"),
        
        # Hidden stores for data
        dcc.Store(id='match-data-store'),
        dcc.Store(id='player-data-store'),
        dcc.Store(id='dreamxi-store'),
    ], style={'backgroundColor': '#0f172a', 'minHeight': '100vh', 'padding': '20px'})
])

# Import all callbacks
from callbacks.season_callbacks import register_season_callbacks
from callbacks.match_callbacks import register_match_callbacks
from callbacks.player_callbacks import register_player_callbacks
from callbacks.pvp_callbacks import register_pvp_callbacks
from callbacks.pvt_callbacks import register_pvt_callbacks
from callbacks.venue_callbacks import register_venue_callbacks
from callbacks.compare_callbacks import register_compare_callbacks
from callbacks.ml_callbacks import register_ml_callbacks
from callbacks.dreamxi_callbacks import register_dreamxi_callbacks
from callbacks.records_callbacks import register_records_callbacks

# Register all callbacks
register_season_callbacks(app, matches, deliveries)
register_match_callbacks(app, matches, deliveries)
register_player_callbacks(app, matches, deliveries, player_stats)
register_pvp_callbacks(app, matches, deliveries)
register_pvt_callbacks(app, matches, deliveries)
register_venue_callbacks(app, matches, deliveries)
register_compare_callbacks(app, matches, deliveries)
register_ml_callbacks(app, matches, deliveries, predictor, similarity_engine)
register_dreamxi_callbacks(app, matches, deliveries, player_stats)
register_records_callbacks(app, matches, deliveries)

if __name__ == '__main__':
    app.run_server(debug=True, port=8050)