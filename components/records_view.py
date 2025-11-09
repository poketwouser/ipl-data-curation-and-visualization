# components/records_view.py
from dash import html, dcc
import dash_bootstrap_components as dbc

def create_records_tab():
    return html.Div([
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H4("🏆 Championship History", style={'color': '#cbd5e1'}),
                        dcc.Graph(id="championship-timeline")
                    ])
                ], className="stats-card")
            ], width=12),
        ]),
        
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H4("👑 All-Time Leaders", className="card-title", style={'color': '#cbd5e1'}),
                        dbc.Tabs([
                            dbc.Tab(label="Batting", tab_id="batting-records"),
                            dbc.Tab(label="Bowling", tab_id="bowling-records"),
                            dbc.Tab(label="Team", tab_id="team-records"),
                        ], id="records-tabs", active_tab="batting-records"),
                        html.Div(id="records-content")
                    ])
                ], className="stats-card")
            ], width=12),
        ]),
        
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H4("📈 Era Comparison", style={'color': '#cbd5e1'}),
                        dcc.Graph(id="era-comparison-chart")
                    ])
                ], className="stats-card")
            ], width=8),
            
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H4("⚡ Record Breakers", style={'color': '#cbd5e1'}),
                        html.Div(id="record-breakers")
                    ])
                ], className="stats-card")
            ], width=4),
        ]),
    ])