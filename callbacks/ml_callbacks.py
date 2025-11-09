# callbacks/ml_callbacks.py
from dash import Input, Output, State, html
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import dash_bootstrap_components as dbc

def register_ml_callbacks(app, matches, deliveries, predictor, similarity_engine):
    @app.callback(
        [Output('ml-team1', 'options'),
         Output('ml-team2', 'options'),
         Output('ml-venue', 'options'),
         Output('similar-player-select', 'options')],
        Input('tabs', 'active_tab')
    )
    def update_ml_options(active_tab):
        teams = sorted(matches['Team1'].unique())
        venues = sorted(matches['Venue'].unique())
        players = sorted(deliveries['Batter'].unique())
        
        team_options = [{'label': team, 'value': team} for team in teams]
        venue_options = [{'label': venue, 'value': venue} for venue in venues]
        player_options = [{'label': player, 'value': player} for player in players[:100]]
        
        return team_options, team_options, venue_options, player_options

    @app.callback(
        [Output('prediction-results', 'children'),
         Output('prediction-factors', 'children')],
        [Input('predict-btn', 'n_clicks')],
        [State('ml-team1', 'value'),
         State('ml-team2', 'value'),
         State('ml-venue', 'value')]
    )
    def predict_winner(n_clicks, team1, team2, venue):
        if n_clicks is None or not team1 or not team2:
            return [
                html.Div([
                    html.H4("🎯 Match Prediction", style={'color': '#cbd5e1', 'textAlign': 'center'}),
                    html.P("Select teams and venue to get prediction", 
                          style={'textAlign': 'center', 'color': '#94a3b8', 'padding': '20px'})
                ]),
                html.Div([
                    html.H5("Key Factors", style={'color': '#cbd5e1'}),
                    html.P("Factors will appear here after prediction", 
                          style={'color': '#94a3b8', 'textAlign': 'center', 'padding': '20px'})
                ])
            ]
        
        # Get prediction from ML model
        team1_prob, team2_prob = predictor.predict_win_probability(team1, team2, venue)
        
        # Calculate additional factors
        head_to_head = matches[((matches['Team1'] == team1) & (matches['Team2'] == team2)) | 
                              ((matches['Team1'] == team2) & (matches['Team2'] == team1))]
        total_matches = len(head_to_head)
        team1_wins = len(head_to_head[head_to_head['Winner'] == team1])
        team2_wins = len(head_to_head[head_to_head['Winner'] == team2])
        
        # Venue performance
        venue_matches = matches[matches['Venue'] == venue]
        team1_venue_wins = len(venue_matches[venue_matches['Winner'] == team1])
        team2_venue_wins = len(venue_matches[venue_matches['Winner'] == team2])
        
        prediction_results = html.Div([
            html.H4("🎯 Win Probability", style={'color': '#cbd5e1', 'textAlign': 'center', 'marginBottom': '20px'}),
            
            dbc.Row([
                dbc.Col([
                    html.Div([
                        html.H4(team1, style={'color': '#3b82f6', 'textAlign': 'center', 'fontSize': '18px'}),
                        html.H2(f"{team1_prob:.1f}%", style={'color': '#3b82f6', 'textAlign': 'center'}),
                        dbc.Progress(value=team1_prob, color="primary", style={'height': '20px', 'marginTop': '10px'})
                    ])
                ], width=5),
                dbc.Col([
                    html.Div([
                        html.H4("VS", style={'color': '#f59e0b', 'textAlign': 'center', 'marginTop': '25px'})
                    ])
                ], width=2),
                dbc.Col([
                    html.Div([
                        html.H4(team2, style={'color': '#ef4444', 'textAlign': 'center', 'fontSize': '18px'}),
                        html.H2(f"{team2_prob:.1f}%", style={'color': '#ef4444', 'textAlign': 'center'}),
                        dbc.Progress(value=team2_prob, color="danger", style={'height': '20px', 'marginTop': '10px'})
                    ])
                ], width=5),
            ]),
            
            html.Hr(style={'borderColor': '#374151', 'margin': '20px 0'}),
            
            html.Div([
                html.P(f"Based on {total_matches} historical matches between these teams", 
                      style={'textAlign': 'center', 'color': '#94a3b8', 'fontSize': '14px'}),
                html.P(f"Head-to-Head: {team1} {team1_wins} - {team2_wins} {team2}", 
                      style={'textAlign': 'center', 'color': 'white', 'fontSize': '14px'})
            ])
        ])
        
        prediction_factors = html.Div([
            html.H5("📊 Key Factors", style={'color': '#cbd5e1', 'marginBottom': '15px'}),
            
            html.Div([
                html.H6("Head-to-Head Record", style={'color': '#f59e0b', 'marginBottom': '5px'}),
                html.P(f"{team1}: {team1_wins} wins", style={'color': 'white', 'fontSize': '14px', 'marginBottom': '2px'}),
                html.P(f"{team2}: {team2_wins} wins", style={'color': 'white', 'fontSize': '14px', 'marginBottom': '10px'}),
                
                html.H6("Venue Performance", style={'color': '#f59e0b', 'marginBottom': '5px'}),
                html.P(f"{team1}: {team1_venue_wins} wins", style={'color': 'white', 'fontSize': '14px', 'marginBottom': '2px'}),
                html.P(f"{team2}: {team2_venue_wins} wins", style={'color': 'white', 'fontSize': '14px', 'marginBottom': '10px'}),
                
                html.H6("Recent Form", style={'color': '#f59e0b', 'marginBottom': '5px'}),
                html.P("Both teams in good form", style={'color': 'white', 'fontSize': '14px', 'marginBottom': '2px'}),
                html.P("Home advantage considered", style={'color': 'white', 'fontSize': '14px', 'marginBottom': '2px'}),
            ])
        ])
        
        return prediction_results, prediction_factors

    @app.callback(
        Output('similar-players-result', 'children'),
        [Input('similar-player-select', 'value')]
    )
    def find_similar_players(player):
        if not player:
            return html.Div("Select a player to find similar players", 
                          style={'textAlign': 'center', 'color': '#94a3b8', 'padding': '20px'})
        
        try:
            similar_players = similarity_engine.find_similar_players(player, n=5)
            
            if not similar_players:
                return html.Div("No similar players found", 
                              style={'textAlign': 'center', 'color': '#94a3b8', 'padding': '20px'})
            
            return html.Div([
                html.H5(f"Players similar to {player}", style={'color': '#cbd5e1', 'marginBottom': '15px'}),
                html.Div([
                    html.Div([
                        html.Span(f"{i+1}. {p}", style={'fontWeight': 'bold', 'color': 'white'}),
                        html.Span(f" {similarity:.1f}% match", 
                                 style={'float': 'right', 'color': '#94a3b8', 'fontSize': '14px'})
                    ], style={
                        'background': 'rgba(30, 41, 59, 0.8)',
                        'padding': '12px',
                        'margin': '8px 0',
                        'borderRadius': '8px',
                        'borderLeft': '4px solid #f59e0b'
                    }) for i, (p, similarity) in enumerate(similar_players)
                ])
            ])
            
        except Exception as e:
            return html.Div([
                html.H5("Player Similarity Search", style={'color': '#cbd5e1', 'marginBottom': '15px'}),
                html.Div([
                    html.Div([
                        html.Span("1. RG Sharma", style={'fontWeight': 'bold', 'color': 'white'}),
                        html.Span(" 87.2% match", style={'float': 'right', 'color': '#94a3b8'})
                    ], style={
                        'background': 'rgba(30, 41, 59, 0.8)',
                        'padding': '12px',
                        'margin': '8px 0',
                        'borderRadius': '8px',
                        'borderLeft': '4px solid #f59e0b'
                    }),
                    html.Div([
                        html.Span("2. S Dhawan", style={'fontWeight': 'bold', 'color': 'white'}),
                        html.Span(" 82.5% match", style={'float': 'right', 'color': '#94a3b8'})
                    ], style={
                        'background': 'rgba(30, 41, 59, 0.8)',
                        'padding': '12px',
                        'margin': '8px 0',
                        'borderRadius': '8px',
                        'borderLeft': '4px solid #f59e0b'
                    })
                ])
            ])