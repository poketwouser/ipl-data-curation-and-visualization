# components/compare_view.py
from dash import html, dcc
import dash_bootstrap_components as dbc

def create_compare_tab():
    return html.Div([
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H4("Comparison Options", className="card-title", style={'color': '#cbd5e1'}),
                        dbc.Row([
                            dbc.Col([
                                dcc.Dropdown(
                                    id='compare-type',
                                    options=[
                                        {'label': 'Seasons', 'value': 'seasons'},
                                        {'label': 'Teams', 'value': 'teams'},
                                        {'label': 'Eras', 'value': 'eras'}
                                    ],
                                    value='seasons'
                                )
                            ], width=4),
                            dbc.Col([
                                dcc.Dropdown(
                                    id='compare-option1',
                                    placeholder="Select first option"
                                )
                            ], width=4),
                            dbc.Col([
                                dcc.Dropdown(
                                    id='compare-option2',
                                    placeholder="Select second option"
                                )
                            ], width=4),
                        ]),
                    ])
                ], className="stats-card")
            ], width=12),
        ]),
        
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H4("📊 Statistical Comparison", style={'color': '#cbd5e1'}),
                        dcc.Graph(id="compare-stats-chart")
                    ])
                ], className="stats-card")
            ], width=12),
        ]),
        
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H4("🎯 Performance Metrics", style={'color': '#cbd5e1'}),
                        dcc.Graph(id="compare-metrics-radar")
                    ])
                ], className="stats-card")
            ], width=6),
            
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H4("📈 Trend Analysis", style={'color': '#cbd5e1'}),
                        dcc.Graph(id="compare-trend-chart")
                    ])
                ], className="stats-card")
            ], width=6),
        ]),
    ])