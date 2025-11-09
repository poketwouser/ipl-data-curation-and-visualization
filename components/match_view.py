# components/match_view.py
from dash import html, dcc
import dash_bootstrap_components as dbc

def create_match_tab():
    return html.Div([
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H4("Match Filters", className="card-title", style={'color': '#cbd5e1'}),
                        dbc.Row([
                            dbc.Col([
                                dcc.Dropdown(
                                    id='match-season-select',
                                    options=[],
                                    placeholder="Select Season"
                                )
                            ], width=4),
                            dbc.Col([
                                dcc.Dropdown(
                                    id='team1-select',
                                    options=[],
                                    placeholder="Team 1"
                                )
                            ], width=4),
                            dbc.Col([
                                dcc.Dropdown(
                                    id='team2-select',
                                    options=[],
                                    placeholder="Team 2"
                                )
                            ], width=4),
                        ]),
                    ])
                ], className="stats-card")
            ], width=12),
        ]),
        
        dbc.Row([
            dbc.Col([
                html.Div(id="match-cards-container")
            ], width=12),
        ]),
        
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H4("📊 Detailed Match Analysis", style={'color': '#cbd5e1'}),
                        html.Div(id="match-detail-view")
                    ])
                ], className="stats-card")
            ], width=12),
        ]),
    ])