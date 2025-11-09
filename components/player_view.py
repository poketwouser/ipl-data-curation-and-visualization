# components/player_view.py
from dash import html, dcc
import dash_bootstrap_components as dbc

def create_player_tab():
    return html.Div([
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H4("Player Selection", className="card-title", style={'color': '#cbd5e1'}),
                        dcc.Dropdown(
                            id='player-select',
                            options=[],
                            value='V Kohli',
                            className="mb-3"
                        ),
                    ])
                ], className="stats-card")
            ], width=6),
            
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H4("Player Profile", id="player-profile-title", style={'color': '#cbd5e1'}),
                        html.Div(id="player-stats-summary")
                    ])
                ], className="stats-card")
            ], width=6),
        ]),
        
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H4("📈 Career Progression", style={'color': '#cbd5e1'}),
                        dcc.Graph(id="player-career-chart")
                    ])
                ], className="stats-card")
            ], width=12),
        ]),
        
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H4("🎯 Performance Radar", style={'color': '#cbd5e1'}),
                        dcc.Graph(id="player-radar-chart")
                    ])
                ], className="stats-card")
            ], width=6),
            
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H4("🏟️ Venue Performance", style={'color': '#cbd5e1'}),
                        dcc.Graph(id="player-venue-chart")
                    ])
                ], className="stats-card")
            ], width=6),
        ]),
    ])