# components/season_view.py
from dash import html, dcc
import dash_bootstrap_components as dbc

def create_season_tab():
    return html.Div([
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H4("Select Season", className="card-title", style={'color': '#cbd5e1'}),
                        dcc.Dropdown(
                            id='season-select',
                            options=[],
                            value='2020',
                            className="mb-3"
                        ),
                    ])
                ], className="stats-card")
            ], width=4),
            
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H4("Season Champion", id="champion-title", style={'color': '#cbd5e1'}),
                        html.H3(id="champion-team", className="animated-number"),
                        html.P(id="champion-details", style={'color': '#94a3b8'})
                    ])
                ], className="stats-card")
            ], width=8),
        ]),
        
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H4("🏏 Top Run Scorers", style={'color': '#cbd5e1'}),
                        html.Div(id="top-batsmen")
                    ])
                ], className="stats-card")
            ], width=6),
            
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H4("🎯 Top Wicket Takers", style={'color': '#cbd5e1'}),
                        html.Div(id="top-bowlers")
                    ])
                ], className="stats-card")
            ], width=6),
        ]),
        
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H4("📈 Season Statistics", style={'color': '#cbd5e1'}),
                        dcc.Graph(id="season-stats-chart")
                    ])
                ], className="stats-card")
            ], width=12),
        ]),
        
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H4("🎪 Boundary Analysis", style={'color': '#cbd5e1'}),
                        dcc.Graph(id="boundary-chart")
                    ])
                ], className="stats-card")
            ], width=8),
            
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H4("🎲 Toss Impact", style={'color': '#cbd5e1'}),
                        dcc.Graph(id="toss-impact-chart")
                    ])
                ], className="stats-card")
            ], width=4),
        ]),
    ])