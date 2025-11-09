# callbacks/pvt_callbacks.py
from dash import Input, Output, State, html
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

def register_pvt_callbacks(app, matches, deliveries):
    @app.callback(
        [Output('pvt-player-select', 'options'),
         Output('pvt-team-select', 'options')],
        Input('tabs', 'active_tab')
    )
    def update_pvt_options(active_tab):
        players = sorted(deliveries['Batter'].unique())
        teams = sorted(matches['Team1'].unique())
        
        player_options = [{'label': player, 'value': player} for player in players[:100]]
        team_options = [{'label': team, 'value': team} for team in teams]
        
        return player_options, team_options

    @app.callback(
        Output('pvt-summary', 'children'),
        [Input('pvt-player-select', 'value'),
         Input('pvt-team-select', 'value')]
    )
    def update_pvt_summary(player, team):
        if not player or not team:
            return "Select a player and team to view performance"
            
        player_vs_team = deliveries[
            (deliveries['Batter'] == player) & 
            (deliveries['Bowling_Team'] == team)
        ]
        
        if player_vs_team.empty:
            return html.Div("No data available for this matchup", 
                          style={'textAlign': 'center', 'color': '#94a3b8', 'padding': '20px'})
        
        total_runs = player_vs_team['Batsman_Runs'].sum()
        total_balls = len(player_vs_team[~player_vs_team['Extras_Type'].isin(['Wides', 'Noballs'])])
        strike_rate = (total_runs / total_balls * 100) if total_balls > 0 else 0
        dismissals = len(player_vs_team[
            (player_vs_team['Is_Wicket'] == 1) & 
            (player_vs_team['Player_Dismissed'] == player)
        ])
        average = total_runs / dismissals if dismissals > 0 else total_runs
        boundaries = len(player_vs_team[player_vs_team['Batsman_Runs'].isin([4, 6])])
        
        return html.Div([
            html.H4(f"{player} vs {team}", style={'color': '#f59e0b', 'textAlign': 'center', 'marginBottom': '20px'}),
            dbc.Row([
                dbc.Col([
                    html.Div([
                        html.H3(f"{int(total_runs)}", style={'color': '#f59e0b', 'textAlign': 'center'}),
                        html.P("Total Runs", style={'textAlign': 'center', 'color': '#94a3b8'})
                    ])
                ], width=4),
                dbc.Col([
                    html.Div([
                        html.H3(f"{strike_rate:.1f}", style={'color': '#10b981', 'textAlign': 'center'}),
                        html.P("Strike Rate", style={'textAlign': 'center', 'color': '#94a3b8'})
                    ])
                ], width=4),
                dbc.Col([
                    html.Div([
                        html.H3(f"{boundaries}", style={'color': '#ef4444', 'textAlign': 'center'}),
                        html.P("Boundaries", style={'textAlign': 'center', 'color': '#94a3b8'})
                    ])
                ], width=4),
            ]),
            html.Hr(style={'borderColor': '#374151', 'margin': '20px 0'}),
            dbc.Row([
                dbc.Col([
                    html.P(f"🏏 Matches: {player_vs_team['Match_Id'].nunique()}", 
                          style={'color': 'white', 'textAlign': 'center'}),
                ], width=6),
                dbc.Col([
                    html.P(f"🎯 Average: {average:.1f}", 
                          style={'color': 'white', 'textAlign': 'center'}),
                ], width=6),
            ])
        ])

    @app.callback(
        Output('pvt-dismissal-chart', 'figure'),
        [Input('pvt-player-select', 'value'),
         Input('pvt-team-select', 'value')]
    )
    def update_pvt_dismissal_chart(player, team):
        if not player or not team:
            return go.Figure()
            
        player_vs_team = deliveries[
            (deliveries['Batter'] == player) & 
            (deliveries['Bowling_Team'] == team) &
            (deliveries['Is_Wicket'] == 1) &
            (deliveries['Player_Dismissed'] == player)
        ]
        
        if player_vs_team.empty:
            # Return empty chart with message
            fig = go.Figure()
            fig.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font_color='white',
                title={'text': 'No Dismissal Data Available', 'x': 0.5}
            )
            return fig
        
        dismissal_counts = player_vs_team['Dismissal_Kind'].value_counts()
        
        fig = px.pie(
            values=dismissal_counts.values,
            names=dismissal_counts.index,
            title=f'Dismissal Types - {player} vs {team}',
            color_discrete_sequence=px.colors.sequential.Viridis
        )
        
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='white',
            title_font_color='white'
        )
        
        return fig

    @app.callback(
        Output('pvt-timeline-chart', 'figure'),
        [Input('pvt-player-select', 'value'),
         Input('pvt-team-select', 'value')]
    )
    def update_pvt_timeline_chart(player, team):
        if not player or not team:
            return go.Figure()
            
        player_vs_team = deliveries[
            (deliveries['Batter'] == player) & 
            (deliveries['Bowling_Team'] == team)
        ]
        
        if player_vs_team.empty:
            return go.Figure()
        
        # Get match dates and runs
        match_performance = player_vs_team.merge(matches[['Id', 'Date']], 
                                               left_on='Match_Id', right_on='Id')
        match_runs = match_performance.groupby(['Date', 'Match_Id']).agg({
            'Batsman_Runs': 'sum'
        }).reset_index()
        
        match_runs['Date'] = pd.to_datetime(match_runs['Date'])
        match_runs = match_runs.sort_values('Date')
        
        fig = px.scatter(match_runs, x='Date', y='Batsman_Runs',
                         title=f'{player} vs {team} - Match Performance Timeline',
                         size='Batsman_Runs', color='Batsman_Runs',
                         color_continuous_scale='Viridis')
        
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='white',
            title_font_color='white',
            xaxis_title="Match Date",
            yaxis_title="Runs Scored"
        )
        
        return fig