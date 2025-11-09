# components/pvp_view.py
from dash import html, dcc
import dash_bootstrap_components as dbc

def create_pvp_tab():
    return html.Div([
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H4("Select Players", className="card-title", style={'color': '#cbd5e1'}),
                        dbc.Row([
                            dbc.Col([
                                dcc.Dropdown(
                                    id='player1-select',
                                    options=[],
                                    value='V Kohli',
                                    placeholder="Select Player 1"
                                )
                            ], width=6),
                            dbc.Col([
                                dcc.Dropdown(
                                    id='player2-select',
                                    options=[],
                                    value='RG Sharma',
                                    placeholder="Select Player 2"
                                )
                            ], width=6),
                        ]),
                    ])
                ], className="stats-card")
            ], width=12),
        ]),
        
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H4("⚔️ Head-to-Head Comparison", style={'color': '#cbd5e1'}),
                        html.Div(id="pvp-comparison")
                    ])
                ], className="stats-card")
            ], width=12),
        ]),
        
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H4("📊 Statistical Comparison", style={'color': '#cbd5e1'}),
                        dcc.Graph(id="pvp-stats-chart")
                    ])
                ], className="stats-card")
            ], width=12),
        ]),
    ])