# components/dreamxi_view.py
from dash import html, dcc
import dash_bootstrap_components as dbc

def create_dreamxi_tab():
    return html.Div([
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H4("🌟 Dream XI Builder", className="card-title", style={'color': '#cbd5e1'}),
                        html.P("Create your ultimate IPL fantasy team with AI-powered suggestions", 
                              style={'color': '#94a3b8'}),
                        
                        dbc.Row([
                            dbc.Col([
                                dbc.Button("Auto-Generate Team", id="auto-generate-btn", 
                                          color="success", className="me-2", style={'width': '100%'}),
                            ], width=6),
                            dbc.Col([
                                dbc.Button("Clear Team", id="clear-team-btn", 
                                          color="warning", className="me-2", style={'width': '100%'}),
                            ], width=6),
                        ]),
                    ])
                ], className="dreamxi-card")
            ], width=12),
        ]),
        
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H4("Your Dream XI", id="dreamxi-title", style={'color': '#cbd5e1'}),
                        html.Div(id="dreamxi-team")
                    ])
                ], className="stats-card")
            ], width=8),
            
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H4("📊 Team Balance", style={'color': '#cbd5e1'}),
                        dcc.Graph(id="team-balance-radar")
                    ])
                ], className="stats-card")
            ], width=4),
        ]),
    ])