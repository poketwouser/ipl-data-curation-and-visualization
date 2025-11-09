# callbacks/match_callbacks.py
from dash import Input, Output, State, html
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

def register_match_callbacks(app, matches, deliveries):
    @app.callback(
        [Output('match-season-select', 'options'),
         Output('team1-select', 'options'),
         Output('team2-select', 'options')],
        Input('tabs', 'active_tab')
    )
    def update_match_filters(active_tab):
        seasons = sorted(matches['Season'].unique(), reverse=True)
        teams = sorted(matches['Team1'].unique())
        
        season_options = [{'label': f'Season {s}', 'value': s} for s in seasons]
        team_options = [{'label': team, 'value': team} for team in teams]
        
        return season_options, team_options, team_options

    @app.callback(
        Output('match-cards-container', 'children'),
        [Input('match-season-select', 'value'),
         Input('team1-select', 'value'),
         Input('team2-select', 'value')]
    )
    def update_match_cards(season, team1, team2):
        filtered_matches = matches.copy()
        
        if season:
            filtered_matches = filtered_matches[filtered_matches['Season'] == season]
        if team1:
            filtered_matches = filtered_matches[(filtered_matches['Team1'] == team1) | (filtered_matches['Team2'] == team1)]
        if team2:
            filtered_matches = filtered_matches[(filtered_matches['Team1'] == team2) | (filtered_matches['Team2'] == team2)]
        
        if filtered_matches.empty:
            return html.Div("No matches found for the selected filters", 
                          style={'textAlign': 'center', 'color': '#94a3b8', 'padding': '40px'})
        
        match_cards = []
        for _, match in filtered_matches.iterrows():
            card_color = '#3b82f6' if pd.notna(match['Winner']) else '#6b7280'
            
            badges = []
            if match['Super_Over'] == 'Y':
                badges.append(html.Span("⚡ SUPER OVER", style={
                    'background': 'linear-gradient(45deg, #FF4500, #FF8C00)',
                    'color': 'white', 'padding': '4px 8px', 'borderRadius': '12px',
                    'fontSize': '10px', 'fontWeight': 'bold', 'marginLeft': '5px'
                }))
            if match['Match_Type'] == 'Final':
                badges.append(html.Span("🏆 FINAL", style={
                    'background': 'linear-gradient(45deg, #B22222, #DC143C)',
                    'color': 'white', 'padding': '4px 8px', 'borderRadius': '12px',
                    'fontSize': '10px', 'fontWeight': 'bold', 'marginLeft': '5px'
                }))
            
            match_card = html.Div([
                dbc.Row([
                    dbc.Col([
                        html.H5(f"{match['Team1']} vs {match['Team2']}", 
                               style={'color': 'white', 'marginBottom': '5px'}),
                        html.P(f"{match['Venue']} • {pd.to_datetime(match['Date']).strftime('%d %b %Y')}", 
                              style={'color': '#94a3b8', 'marginBottom': '5px', 'fontSize': '14px'}),
                        html.Div(badges)
                    ], width=8),
                    dbc.Col([
                        html.H6("Result", style={'color': '#94a3b8', 'fontSize': '12px'}),
                        html.P(match['Result'] if pd.notna(match['Result']) else 'No Result', 
                              style={'color': 'white', 'fontSize': '14px', 'marginBottom': '5px'}),
                        html.P(f"Winner: {match['Winner']}" if pd.notna(match['Winner']) else 'No Winner',
                              style={'color': '#f59e0b', 'fontSize': '12px', 'marginBottom': '0'})
                    ], width=4, style={'textAlign': 'right'}),
                ])
            ], style={
                'background': 'rgba(30, 41, 59, 0.8)',
                'borderRadius': '12px',
                'padding': '15px',
                'margin': '10px 0',
                'borderLeft': f'4px solid {card_color}',
                'transition': 'all 0.3s ease',
                'cursor': 'pointer'
            }, className="match-card")
            
            match_cards.append(match_card)
        
        return match_cards

    @app.callback(
        Output('match-detail-view', 'children'),
        [Input('match-cards-container', 'children')],
        [State('match-season-select', 'value'),
         State('team1-select', 'value'),
         State('team2-select', 'value')]
    )
    def update_match_detail(match_cards, season, team1, team2):
        return html.Div([
            html.H4("Select a match to view detailed analysis", 
                   style={'textAlign': 'center', 'color': '#94a3b8', 'padding': '40px'}),
            html.P("Click on any match card above to see detailed scorecard and analysis",
                  style={'textAlign': 'center', 'color': '#64748b'})
        ])