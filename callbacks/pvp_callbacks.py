# callbacks/pvp_callbacks.py
from dash import Input, Output, State, html
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

def register_pvp_callbacks(app, matches, deliveries):
    @app.callback(
        [Output('player1-select', 'options'),
         Output('player2-select', 'options')],
        Input('tabs', 'active_tab')
    )
    def update_pvp_options(active_tab):
        players = sorted(deliveries['Batter'].unique())
        player_options = [{'label': player, 'value': player} for player in players[:100]]
        return player_options, player_options

    @app.callback(
        Output('pvp-comparison', 'children'),
        [Input('player1-select', 'value'),
         Input('player2-select', 'value')]
    )
    def update_pvp_comparison(player1, player2):
        if not player1 or not player2:
            return "Select two players to compare"
            
        # Get stats for both players
        p1_data = deliveries[deliveries['Batter'] == player1]
        p2_data = deliveries[deliveries['Batter'] == player2]
        
        p1_runs = p1_data['Batsman_Runs'].sum()
        p2_runs = p2_data['Batsman_Runs'].sum()
        p1_matches = p1_data['Match_Id'].nunique()
        p2_matches = p2_data['Match_Id'].nunique()
        
        # Calculate strike rates
        p1_balls = len(p1_data[~p1_data['Extras_Type'].isin(['Wides', 'Noballs'])])
        p2_balls = len(p2_data[~p2_data['Extras_Type'].isin(['Wides', 'Noballs'])])
        p1_sr = (p1_runs / p1_balls * 100) if p1_balls > 0 else 0
        p2_sr = (p2_runs / p2_balls * 100) if p2_balls > 0 else 0
        
        return html.Div([
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.H4(player1, style={'color': '#3b82f6', 'textAlign': 'center'}),
                            html.H2(f"{p1_runs}", style={'color': '#f59e0b', 'textAlign': 'center'}),
                            html.P("Total Runs", style={'textAlign': 'center', 'color': '#94a3b8'}),
                            html.P(f"Matches: {p1_matches}", style={'textAlign': 'center', 'color': 'white'}),
                            html.P(f"Strike Rate: {p1_sr:.1f}", style={'textAlign': 'center', 'color': 'white'})
                        ])
                    ], className="stats-card")
                ], width=6),
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.H4(player2, style={'color': '#ef4444', 'textAlign': 'center'}),
                            html.H2(f"{p2_runs}", style={'color': '#f59e0b', 'textAlign': 'center'}),
                            html.P("Total Runs", style={'textAlign': 'center', 'color': '#94a3b8'}),
                            html.P(f"Matches: {p2_matches}", style={'textAlign': 'center', 'color': 'white'}),
                            html.P(f"Strike Rate: {p2_sr:.1f}", style={'textAlign': 'center', 'color': 'white'})
                        ])
                    ], className="stats-card")
                ], width=6),
            ])
        ])

    @app.callback(
        Output('pvp-stats-chart', 'figure'),
        [Input('player1-select', 'value'),
         Input('player2-select', 'value')]
    )
    def update_pvp_stats_chart(player1, player2):
        if not player1 or not player2:
            return go.Figure()
            
        p1_data = deliveries[deliveries['Batter'] == player1]
        p2_data = deliveries[deliveries['Batter'] == player2]
        
        # Calculate multiple statistics
        stats = ['Total Runs', 'Matches', 'Average', 'Strike Rate', 'Boundaries']
        p1_values = [
            p1_data['Batsman_Runs'].sum(),
            p1_data['Match_Id'].nunique(),
            p1_data['Batsman_Runs'].sum() / p1_data['Match_Id'].nunique() if p1_data['Match_Id'].nunique() > 0 else 0,
            (p1_data['Batsman_Runs'].sum() / len(p1_data[~p1_data['Extras_Type'].isin(['Wides', 'Noballs'])]) * 100) 
            if len(p1_data[~p1_data['Extras_Type'].isin(['Wides', 'Noballs'])]) > 0 else 0,
            len(p1_data[p1_data['Batsman_Runs'].isin([4, 6])])
        ]
        p2_values = [
            p2_data['Batsman_Runs'].sum(),
            p2_data['Match_Id'].nunique(),
            p2_data['Batsman_Runs'].sum() / p2_data['Match_Id'].nunique() if p2_data['Match_Id'].nunique() > 0 else 0,
            (p2_data['Batsman_Runs'].sum() / len(p2_data[~p2_data['Extras_Type'].isin(['Wides', 'Noballs'])]) * 100) 
            if len(p2_data[~p2_data['Extras_Type'].isin(['Wides', 'Noballs'])]) > 0 else 0,
            len(p2_data[p2_data['Batsman_Runs'].isin([4, 6])])
        ]
        
        fig = go.Figure(data=[
            go.Bar(name=player1, x=stats, y=p1_values, marker_color='#3b82f6'),
            go.Bar(name=player2, x=stats, y=p2_values, marker_color='#ef4444')
        ])
        
        fig.update_layout(
            barmode='group',
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='white',
            title=f'Statistical Comparison: {player1} vs {player2}'
        )
        
        return fig