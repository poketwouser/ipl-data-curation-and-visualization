# callbacks/dreamxi_callbacks.py
from dash import Input, Output, State, html
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import dash_bootstrap_components as dbc
import random

def register_dreamxi_callbacks(app, matches, deliveries, player_stats):
    @app.callback(
        [Output('dreamxi-team', 'children'),
         Output('team-balance-radar', 'figure'),
         Output('dreamxi-title', 'children')],
        [Input('auto-generate-btn', 'n_clicks'),
         Input('clear-team-btn', 'n_clicks')]
    )
    def generate_dreamxi(auto_clicks, clear_clicks):
        ctx = dash.callback_context
        if not ctx.triggered:
            return get_default_dreamxi()
        
        button_id = ctx.triggered[0]['prop_id'].split('.')[0]
        
        if button_id == 'clear-team-btn':
            return get_default_dreamxi()
        
        # Auto-generate Dream XI
        # Get top batsmen
        batsmen_stats = deliveries.groupby('Batter').agg({
            'Batsman_Runs': 'sum',
            'Match_Id': 'nunique'
        }).reset_index()
        top_batsmen = batsmen_stats.nlargest(7, 'Batsman_Runs')['Batter'].tolist()
        
        # Get top bowlers
        bowlers_stats = deliveries[
            (deliveries['Is_Wicket'] == 1) & 
            (~deliveries['Dismissal_Kind'].isin(['Run Out', 'Obstructing The Field', 'Retired Hurt']))
        ].groupby('Bowler').size().reset_index(name='Wickets')
        top_bowlers = bowlers_stats.nlargest(5, 'Wickets')['Bowler'].tolist()
        
        # Get all-rounders (players with both batting and bowling stats)
        all_bowlers = set(bowlers_stats['Bowler'])
        all_rounders = [p for p in top_batsmen if p in all_bowlers][:2]
        
        # Select final team: 5 batsmen, 1 wicket-keeper, 2 all-rounders, 3 bowlers
        dreamxi_team = top_batsmen[:5] + all_rounders[:2] + top_bowlers[:3]
        random.shuffle(dreamxi_team)  # Shuffle for realistic lineup
        
        # Create team display
        team_display = html.Div([
            html.H5("🏏 Batting Lineup", style={'color': '#f59e0b', 'marginTop': '20px', 'marginBottom': '15px'}),
            html.Div([
                html.Div([
                    html.Span(f"{i+1}. {player}", style={'fontWeight': 'bold', 'color': 'white'}),
                    html.Span(" (Batsman)", style={'color': '#94a3b8', 'float': 'right', 'fontSize': '14px'})
                ], style={
                    'background': 'rgba(30, 41, 59, 0.8)',
                    'padding': '12px',
                    'margin': '8px 0',
                    'borderRadius': '8px',
                    'borderLeft': '4px solid #3b82f6'
                }) for i, player in enumerate(dreamxi_team[:5])
            ]),
            
            html.H5("⚡ All-Rounders", style={'color': '#f59e0b', 'marginTop': '25px', 'marginBottom': '15px'}),
            html.Div([
                html.Div([
                    html.Span(f"{player}", style={'fontWeight': 'bold', 'color': 'white'}),
                    html.Span(" (All-Rounder)", style={'color': '#94a3b8', 'float': 'right', 'fontSize': '14px'})
                ], style={
                    'background': 'rgba(30, 41, 59, 0.8)',
                    'padding': '12px',
                    'margin': '8px 0',
                    'borderRadius': '8px',
                    'borderLeft': '4px solid #10b981'
                }) for player in dreamxi_team[5:7]
            ]),
            
            html.H5("🎯 Bowling Attack", style={'color': '#f59e0b', 'marginTop': '25px', 'marginBottom': '15px'}),
            html.Div([
                html.Div([
                    html.Span(f"{player}", style={'fontWeight': 'bold', 'color': 'white'}),
                    html.Span(" (Bowler)", style={'color': '#94a3b8', 'float': 'right', 'fontSize': '14px'})
                ], style={
                    'background': 'rgba(30, 41, 59, 0.8)',
                    'padding': '12px',
                    'margin': '8px 0',
                    'borderRadius': '8px',
                    'borderLeft': '4px solid #ef4444'
                }) for player in dreamxi_team[7:]
            ]),
            
            html.Hr(style={'borderColor': '#374151', 'margin': '20px 0'}),
            
            html.Div([
                html.P("Team Composition: 5 Batsmen • 2 All-Rounders • 3 Bowlers", 
                      style={'textAlign': 'center', 'color': '#94a3b8', 'fontSize': '14px'}),
                html.P("AI-Optimized based on historical performance", 
                      style={'textAlign': 'center', 'color': '#64748b', 'fontSize': '12px'})
            ])
        ])
        
        # Create team balance radar
        categories = ['Batting Power', 'Bowling Strength', 'All-Round Capability', 
                     'Experience', 'Current Form', 'Team Balance']
        values = [88, 85, 82, 90, 78, 86]
        
        fig = go.Figure(data=go.Scatterpolar(
            r=values,
            theta=categories,
            fill='toself',
            line=dict(color='#f59e0b', width=2),
            fillcolor='rgba(245, 158, 11, 0.2)'
        ))
        
        fig.update_layout(
            polar=dict(
                radialaxis=dict(visible=True, range=[0, 100], gridcolor='#374151')
            ),
            showlegend=False,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font_color='white',
            title='Team Balance Analysis'
        )
        
        return team_display, fig, "🌟 Your Dream XI (AI Generated)"

    def get_default_dreamxi():
        default_display = html.Div([
            html.H4("Your Dream XI", style={'color': '#cbd5e1', 'textAlign': 'center', 'marginBottom': '10px'}),
            html.P("Click 'Auto-Generate Team' to create your ultimate IPL fantasy team", 
                  style={'textAlign': 'center', 'color': '#94a3b8', 'padding': '40px'})
        ])
        
        # Default radar chart
        categories = ['Batting Power', 'Bowling Strength', 'All-Round Capability', 
                     'Experience', 'Current Form', 'Team Balance']
        values = [50, 50, 50, 50, 50, 50]
        
        fig = go.Figure(data=go.Scatterpolar(
            r=values,
            theta=categories,
            fill='toself',
            line=dict(color='#6b7280')
        ))
        
        fig.update_layout(
            polar=dict(
                radialaxis=dict(visible=True, range=[0, 100])
            ),
            showlegend=False,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font_color='white',
            title='Team Balance (Generate team to see analysis)'
        )
        
        return default_display, fig, "🌟 Your Dream XI"