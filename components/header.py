# components/header.py
from dash import html, dcc
import dash_bootstrap_components as dbc

def create_header(matches):
    total_matches = len(matches)
    super_overs = len(matches[matches['Super_Over'] == 'Y'])
    teams_count = len(matches['Team1'].unique())
    
    # Calculate champions count (Mumbai Indians have most wins)
    champions = matches[matches['Match_Type'] == 'Final']['Winner'].value_counts()
    top_champion_wins = champions.iloc[0] if not champions.empty else 0
    
    return html.Div([
        html.Div([
            html.H1("🏏 IPL Analytics Dashboard", 
                   style={'color': 'white', 'margin': '0', 'fontWeight': 'bold', 'fontSize': '2.5rem'}),
            html.P("Advanced Cricket Intelligence Platform • 2008-2024", 
                  style={'color': '#cbd5e1', 'margin': '0', 'fontSize': '1.2rem'}),
        ], className='ipl-header'),
        
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H4("📊 Total Matches", className="card-title", style={'color': '#cbd5e1'}),
                        html.H2(f"{total_matches}", className="animated-number"),
                        html.P("Across All Seasons", style={'color': '#94a3b8'})
                    ])
                ], className="stats-card")
            ], width=3),
            
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H4("🏆 Championships", className="card-title", style={'color': '#cbd5e1'}),
                        html.H2(f"{top_champion_wins}", className="animated-number"),
                        html.P("Mumbai Indians Lead", style={'color': '#94a3b8'})
                    ])
                ], className="stats-card")
            ], width=3),
            
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H4("⚡ Super Overs", className="card-title", style={'color': '#cbd5e1'}),
                        html.H2(f"{super_overs}", className="animated-number"),
                        html.P("Thrilling Finishes", style={'color': '#94a3b8'})
                    ])
                ], className="stats-card")
            ], width=3),
            
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H4("🎯 Teams", className="card-title", style={'color': '#cbd5e1'}),
                        html.H2(f"{teams_count}", className="animated-number"),
                        html.P("Franchises", style={'color': '#94a3b8'})
                    ])
                ], className="stats-card")
            ], width=3),
        ])
    ])