# callbacks/records_callbacks.py
from dash import Input, Output, State, html
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import dash_bootstrap_components as dbc

def register_records_callbacks(app, matches, deliveries):
    @app.callback(
        Output('championship-timeline', 'figure'),
        Input('tabs', 'active_tab')
    )
    def update_championship_timeline(active_tab):
        champions = matches[matches['Match_Type'] == 'Final'].dropna(subset=['Winner'])
        champion_by_season = champions.groupby('Season')['Winner'].first().reset_index()
        
        # Define team colors
        team_colors = {
            'Mumbai Indians': '#004BA0', 'Chennai Super Kings': '#FFFF00',
            'Kolkata Knight Riders': '#3A225D', 'Sunrisers Hyderabad': '#FF822A',
            'Rajasthan Royals': '#FF1C5B', 'Royal Challengers Bangalore': '#EC1C24'
        }
        
        fig = px.scatter(champion_by_season, x='Season', y='Winner',
                         title='IPL Champions Timeline (2008-2024)',
                         size=[15]*len(champion_by_season),
                         color='Winner', color_discrete_map=team_colors)
        
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='white',
            title_font_color='white',
            showlegend=True,
            xaxis_title="Season",
            yaxis_title="Champion Team",
            height=400
        )
        
        return fig

    @app.callback(
        Output('records-content', 'children'),
        [Input('records-tabs', 'active_tab')]
    )
    def update_records_content(active_tab):
        if active_tab == "batting-records":
            # Calculate top batsmen
            batting_stats = deliveries.groupby('Batter').agg({
                'Batsman_Runs': 'sum',
                'Match_Id': 'nunique',
                'Batsman_Runs': 'mean'
            }).reset_index()
            batting_stats.columns = ['Player', 'Total_Runs', 'Matches', 'Average']
            batting_stats = batting_stats.nlargest(10, 'Total_Runs')
            
            return html.Div([
                html.H5("🏏 Top Run Scorers of All Time", 
                       style={'color': '#f59e0b', 'marginBottom': '20px', 'textAlign': 'center'}),
                dbc.Table([
                    html.Thead([
                        html.Tr([
                            html.Th("Rank", style={'color': '#f59e0b'}),
                            html.Th("Player", style={'color': '#f59e0b'}),
                            html.Th("Runs", style={'color': '#f59e0b'}),
                            html.Th("Matches", style={'color': '#f59e0b'}),
                            html.Th("Average", style={'color': '#f59e0b'})
                        ])
                    ]),
                    html.Tbody([
                        html.Tr([
                            html.Td(i+1, style={'color': 'white', 'fontWeight': 'bold'}),
                            html.Td(row['Player'], style={'color': 'white'}),
                            html.Td(f"{int(row['Total_Runs']):,}", style={'color': '#3b82f6', 'fontWeight': 'bold'}),
                            html.Td(int(row['Matches']), style={'color': 'white'}),
                            html.Td(f"{row['Average']:.1f}", style={'color': '#10b981'})
                        ]) for i, (_, row) in enumerate(batting_stats.iterrows())
                    ])
                ], bordered=True, dark=True, hover=True, responsive=True,
                style={'backgroundColor': 'rgba(30, 41, 59, 0.8)'})
            ])
        
        elif active_tab == "bowling-records":
            # Calculate top bowlers
            bowling_stats = deliveries[
                (deliveries['Is_Wicket'] == 1) & 
                (~deliveries['Dismissal_Kind'].isin(['Run Out', 'Obstructing The Field', 'Retired Hurt']))
            ].groupby('Bowler').size().reset_index(name='Wickets')
            
            bowling_stats = bowling_stats.nlargest(10, 'Wickets')
            
            return html.Div([
                html.H5("🎯 Top Wicket Takers of All Time", 
                       style={'color': '#f59e0b', 'marginBottom': '20px', 'textAlign': 'center'}),
                dbc.Table([
                    html.Thead([
                        html.Tr([
                            html.Th("Rank", style={'color': '#f59e0b'}),
                            html.Th("Player", style={'color': '#f59e0b'}),
                            html.Th("Wickets", style={'color': '#f59e0b'})
                        ])
                    ]),
                    html.Tbody([
                        html.Tr([
                            html.Td(i+1, style={'color': 'white', 'fontWeight': 'bold'}),
                            html.Td(row['Bowler'], style={'color': 'white'}),
                            html.Td(f"{int(row['Wickets'])}", style={'color': '#ef4444', 'fontWeight': 'bold'})
                        ]) for i, (_, row) in enumerate(bowling_stats.iterrows())
                    ])
                ], bordered=True, dark=True, hover=True, responsive=True,
                style={'backgroundColor': 'rgba(30, 41, 59, 0.8)'})
            ])
        
        else:  # team records
            team_wins = matches.groupby('Winner').size().reset_index(name='Wins')
            team_wins = team_wins[team_wins['Winner'].notna()].nlargest(10, 'Wins')
            
            return html.Div([
                html.H5("🏆 Most Successful Teams", 
                       style={'color': '#f59e0b', 'marginBottom': '20px', 'textAlign': 'center'}),
                dbc.Table([
                    html.Thead([
                        html.Tr([
                            html.Th("Rank", style={'color': '#f59e0b'}),
                            html.Th("Team", style={'color': '#f59e0b'}),
                            html.Th("Wins", style={'color': '#f59e0b'})
                        ])
                    ]),
                    html.Tbody([
                        html.Tr([
                            html.Td(i+1, style={'color': 'white', 'fontWeight': 'bold'}),
                            html.Td(row['Winner'], style={'color': 'white'}),
                            html.Td(f"{int(row['Wins'])}", style={'color': '#f59e0b', 'fontWeight': 'bold'})
                        ]) for i, (_, row) in enumerate(team_wins.iterrows())
                    ])
                ], bordered=True, dark=True, hover=True, responsive=True,
                style={'backgroundColor': 'rgba(30, 41, 59, 0.8)'})
            ])

    @app.callback(
        Output('era-comparison-chart', 'figure'),
        Input('tabs', 'active_tab')
    )
    def update_era_comparison(active_tab):
        # Define eras
        era1 = matches[matches['Season'].isin(['2008', '2009', '2010', '2011', '2012'])]
        era2 = matches[matches['Season'].isin(['2013', '2014', '2015', '2016', '2017'])]
        era3 = matches[matches['Season'].isin(['2018', '2019', '2020', '2021', '2022', '2023', '2024'])]
        
        eras = ['2008-2012', '2013-2017', '2018-2024']
        avg_runs = [
            era1[['Team1_Runs', 'Team2_Runs']].mean().mean(),
            era2[['Team1_Runs', 'Team2_Runs']].mean().mean(),
            era3[['Team1_Runs', 'Team2_Runs']].mean().mean()
        ]
        
        sixes_count = [
            len(deliveries[deliveries['Match_Id'].isin(era1['Id']) & (deliveries['Batsman_Runs'] == 6)]),
            len(deliveries[deliveries['Match_Id'].isin(era2['Id']) & (deliveries['Batsman_Runs'] == 6)]),
            len(deliveries[deliveries['Match_Id'].isin(era3['Id']) & (deliveries['Batsman_Runs'] == 6)])
        ]
        
        fig = go.Figure()
        
        fig.add_trace(go.Bar(name='Average Runs', x=eras, y=avg_runs, 
                            marker_color='#3b82f6', yaxis='y'))
        fig.add_trace(go.Scatter(name='Total Sixes', x=eras, y=sixes_count, 
                               line=dict(color='#ef4444', width=4), yaxis='y2'))
        
        fig.update_layout(
            title='Era Comparison: Runs and Sixes',
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='white',
            title_font_color='white',
            xaxis_title="Era",
            yaxis=dict(title='Average Runs', color='#3b82f6'),
            yaxis2=dict(title='Total Sixes', color='#ef4444', overlaying='y', side='right'),
            legend=dict(x=0.02, y=0.98)
        )
        
        return fig

    @app.callback(
        Output('record-breakers', 'children'),
        Input('tabs', 'active_tab')
    )
    def update_record_breakers(active_tab):
        return html.Div([
            html.H5("⚡ Record Breakers", style={'color': '#f59e0b', 'marginBottom': '15px'}),
            
            html.Div([
                html.Div([
                    html.H6("Most Runs in a Season", style={'color': '#3b82f6', 'marginBottom': '5px'}),
                    html.P("V Kohli - 973 runs (2016)", style={'color': 'white', 'fontSize': '14px'})
                ], style={
                    'background': 'rgba(30, 41, 59, 0.8)',
                    'padding': '12px',
                    'margin': '8px 0',
                    'borderRadius': '8px'
                }),
                
                html.Div([
                    html.H6("Highest Individual Score", style={'color': '#ef4444', 'marginBottom': '5px'}),
                    html.P("CH Gayle - 175* (2013)", style={'color': 'white', 'fontSize': '14px'})
                ], style={
                    'background': 'rgba(30, 41, 59, 0.8)',
                    'padding': '12px',
                    'margin': '8px 0',
                    'borderRadius': '8px'
                }),
                
                html.Div([
                    html.H6("Most Wickets in a Season", style={'color': '#10b981', 'marginBottom': '5px'}),
                    html.P("Dwayne Bravo - 32 wickets (2013)", style={'color': 'white', 'fontSize': '14px'})
                ], style={
                    'background': 'rgba(30, 41, 59, 0.8)',
                    'padding': '12px',
                    'margin': '8px 0',
                    'borderRadius': '8px'
                }),
                
                html.Div([
                    html.H6("Fastest Century", style={'color': '#f59e0b', 'marginBottom': '5px'}),
                    html.P("CH Gayle - 30 balls (2013)", style={'color': 'white', 'fontSize': '14px'})
                ], style={
                    'background': 'rgba(30, 41, 59, 0.8)',
                    'padding': '12px',
                    'margin': '8px 0',
                    'borderRadius': '8px'
                })
            ])
        ])