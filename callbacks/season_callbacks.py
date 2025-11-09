# callbacks/season_callbacks.py
from dash import Input, Output, State
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

def register_season_callbacks(app, matches, deliveries):
    @app.callback(
        Output('season-select', 'options'),
        Input('tabs', 'active_tab')
    )
    def update_season_options(active_tab):
        seasons = sorted(matches['Season'].unique(), reverse=True)
        return [{'label': f'Season {s}', 'value': s} for s in seasons]

    @app.callback(
        [Output('champion-title', 'children'),
         Output('champion-team', 'children'),
         Output('champion-details', 'children')],
        [Input('season-select', 'value')]
    )
    def update_champion(season):
        if not season:
            return "Season Champion", "Select Season", "Choose a season to view champion"
            
        season_matches = matches[matches['Season'] == season]
        final_match = season_matches[season_matches['Match_Type'] == 'Final']
        
        if not final_match.empty:
            winner = final_match.iloc[0]['Winner']
            if pd.isna(winner):
                return f"🏆 {season} Champion", "No Winner", "Final match had no result"
                
            runner_up = final_match.iloc[0]['Team1'] if final_match.iloc[0]['Team2'] == winner else final_match.iloc[0]['Team2']
            venue = final_match.iloc[0]['Venue']
            
            return f"🏆 {season} Champion", winner, f"Defeated {runner_up} at {venue}"
        else:
            return "Season Champion", "No Final Data", "Final match data not available"

    @app.callback(
        Output('top-batsmen', 'children'),
        [Input('season-select', 'value')]
    )
    def update_top_batsmen(season):
        if not season:
            return "Select a season to view top batsmen"
            
        season_matches = matches[matches['Season'] == season]
        season_match_ids = season_matches['Id'].tolist()
        season_deliveries = deliveries[deliveries['Match_Id'].isin(season_match_ids)]
        
        batsmen_stats = season_deliveries.groupby('Batter').agg({
            'Batsman_Runs': 'sum',
            'Match_Id': 'nunique'
        }).reset_index()
        
        batsmen_stats = batsmen_stats.nlargest(5, 'Batsman_Runs')
        
        return [
            html.Div([
                html.Span(f"{i+1}. ", style={'color': '#f59e0b', 'fontWeight': 'bold'}),
                html.Span(row['Batter'], style={'fontWeight': 'bold', 'color': 'white'}),
                html.Span(f" - {int(row['Batsman_Runs'])} runs", 
                         style={'float': 'right', 'color': '#94a3b8'})
            ], style={
                'background': 'rgba(30, 41, 59, 0.8)',
                'padding': '10px',
                'margin': '5px 0',
                'borderRadius': '8px',
                'borderLeft': '4px solid #f59e0b'
            }) for i, (_, row) in enumerate(batsmen_stats.iterrows())
        ]

    @app.callback(
        Output('top-bowlers', 'children'),
        [Input('season-select', 'value')]
    )
    def update_top_bowlers(season):
        if not season:
            return "Select a season to view top bowlers"
            
        season_matches = matches[matches['Season'] == season]
        season_match_ids = season_matches['Id'].tolist()
        season_deliveries = deliveries[deliveries['Match_Id'].isin(season_match_ids)]
        
        bowlers_stats = season_deliveries[
            (season_deliveries['Is_Wicket'] == 1) & 
            (~season_deliveries['Dismissal_Kind'].isin(['Run Out', 'Obstructing The Field', 'Retired Hurt']))
        ].groupby('Bowler').size().reset_index(name='Wickets')
        
        bowlers_stats = bowlers_stats.nlargest(5, 'Wickets')
        
        return [
            html.Div([
                html.Span(f"{i+1}. ", style={'color': '#f59e0b', 'fontWeight': 'bold'}),
                html.Span(row['Bowler'], style={'fontWeight': 'bold', 'color': 'white'}),
                html.Span(f" - {int(row['Wickets'])} wickets", 
                         style={'float': 'right', 'color': '#94a3b8'})
            ], style={
                'background': 'rgba(30, 41, 59, 0.8)',
                'padding': '10px',
                'margin': '5px 0',
                'borderRadius': '8px',
                'borderLeft': '4px solid #f59e0b'
            }) for i, (_, row) in enumerate(bowlers_stats.iterrows())
        ]

    @app.callback(
        Output('season-stats-chart', 'figure'),
        [Input('season-select', 'value')]
    )
    def update_season_stats(season):
        if not season:
            return go.Figure()
            
        season_matches = matches[matches['Season'] == season]
        
        stats_data = {
            'Metric': ['Total Matches', 'Super Overs', 'Highest Score', 'Average Runs', 'Wickets/Match'],
            'Value': [
                len(season_matches),
                len(season_matches[season_matches['Super_Over'] == 'Y']),
                season_matches[['Team1_Runs', 'Team2_Runs']].max().max(),
                season_matches[['Team1_Runs', 'Team2_Runs']].mean().mean(),
                season_matches[['Team1_Wickets', 'Team2_Wickets']].mean().mean()
            ]
        }
        
        fig = px.bar(stats_data, x='Value', y='Metric', orientation='h',
                     title=f'Season {season} Statistics',
                     color='Value', color_continuous_scale='Viridis')
        
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='white',
            title_font_color='white',
            showlegend=False
        )
        
        return fig

    @app.callback(
        Output('boundary-chart', 'figure'),
        [Input('season-select', 'value')]
    )
    def update_boundary_chart(season):
        if not season:
            return go.Figure()
            
        season_matches = matches[matches['Season'] == season]
        season_match_ids = season_matches['Id'].tolist()
        season_deliveries = deliveries[deliveries['Match_Id'].isin(season_match_ids)]
        
        boundaries = season_deliveries[season_deliveries['Batsman_Runs'].isin([4, 6])]
        boundary_counts = boundaries['Batsman_Runs'].value_counts()
        
        fig = px.pie(values=boundary_counts.values, names=boundary_counts.index.map({4: 'Fours', 6: 'Sixes'}),
                     title=f'Boundary Distribution - Season {season}',
                     color_discrete_sequence=['#3b82f6', '#ef4444'])
        
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='white',
            title_font_color='white'
        )
        
        return fig

    @app.callback(
        Output('toss-impact-chart', 'figure'),
        [Input('season-select', 'value')]
    )
    def update_toss_impact(season):
        if not season:
            return go.Figure()
            
        season_matches = matches[matches['Season'] == season]
        toss_winners = season_matches[season_matches['Toss_Winner'] == season_matches['Winner']]
        toss_win_percentage = len(toss_winners) / len(season_matches) * 100
        
        fig = go.Figure(go.Indicator(
            mode = "gauge+number+delta",
            value = toss_win_percentage,
            domain = {'x': [0, 1], 'y': [0, 1]},
            title = {'text': "Toss Win -> Match Win %"},
            gauge = {
                'axis': {'range': [None, 100]},
                'bar': {'color': "darkblue"},
                'steps': [
                    {'range': [0, 50], 'color': "lightgray"},
                    {'range': [50, 75], 'color': "gray"}],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 90}}
        ))
        
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='white'
        )
        
        return fig