# components/pvt_view.py
from dash import html, dcc
import dash_bootstrap_components as dbc

def create_pvt_tab():
    return html.Div([
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H4("Player vs Team Analysis", className="card-title", style={'color': '#cbd5e1'}),
                        dbc.Row([
                            dbc.Col([
                                dcc.Dropdown(
                                    id='pvt-player-select',
                                    options=[],
                                    value='V Kohli',
                                    placeholder="Select Player"
                                )
                            ], width=6),
                            dbc.Col([
                                dcc.Dropdown(
                                    id='pvt-team-select',
                                    options=[],
                                    value='Mumbai Indians',
                                    placeholder="Select Team"
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
                        html.H4("🎯 Performance Summary", style={'color': '#cbd5e1'}),
                        html.Div(id="pvt-summary")
                    ])
                ], className="stats-card")
            ], width=6),
            
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H4("📊 Dismissal Analysis", style={'color': '#cbd5e1'}),
                        dcc.Graph(id="pvt-dismissal-chart")
                    ])
                ], className="stats-card")
            ], width=6),
        ]),
        
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H4("📈 Match-by-Match Performance", style={'color': '#cbd5e1'}),
                        dcc.Graph(id="pvt-timeline-chart")
                    ])
                ], className="stats-card")
            ], width=12),
        ]),
    ])