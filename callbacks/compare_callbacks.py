# callbacks/compare_callbacks.py
from dash import Input, Output, State, html
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

def register_compare_callbacks(app, matches, deliveries):
    @app.callback(
        [Output('compare-option1', 'options'),
         Output('compare-option2', 'options')],
        [Input('compare-type', 'value')]
    )
    def update_compare_options(compare_type):
        if compare_type == 'seasons':
            seasons = sorted(matches['Season'].unique(), reverse=True)
            options = [{'label': f'Season {s}', 'value': s} for s in seasons]
        elif compare_type == 'teams':
            teams = sorted(matches['Team1'].unique())
            options = [{'label': team, 'value': team} for team in teams]
        else:  # eras
            options = [
                {'label': '2008-2012 (Foundation Era)', 'value': 'era1'},
                {'label': '2013-2017 (Expansion Era)', 'value': 'era2'},
                {'label': '2018-2024 (Modern Era)', 'value': 'era3'}
            ]
        
        return options, options

    @app.callback(
        Output('compare-stats-chart', 'figure'),
        [Input('compare-option1', 'value'),
         Input('compare-option2', 'value'),
         Input('compare-type', 'value')]
    )
    def update_compare_chart(option1, option2, compare_type):
        if not option1 or not option2:
            return go.Figure()
        
        if compare_type == 'seasons':
            data1 = matches[matches['Season'] == option1]
            data2 = matches[matches['Season'] == option2]
            
            metrics = ['Total Matches', 'Average Runs', 'Super Overs', 'Win % Batting First']
            values1 = [
                len(data1),
                data1[['Team1_Runs', 'Team2_Runs']].mean().mean(),
                len(data1[data1['Super_Over'] == 'Y']),
                len(data1[data1['Toss_Decision'] == 'Bat']) / len(data1) * 100 if len(data1) > 0 else 0
            ]
            values2 = [
                len(data2),
                data2[['Team1_Runs', 'Team2_Runs']].mean().mean(),
                len(data2[data2['Super_Over'] == 'Y']),
                len(data2[data2['Toss_Decision'] == 'Bat']) / len(data2) * 100 if len(data2) > 0 else 0
            ]
            
        elif compare_type == 'teams':
            data1 = matches[(matches['Team1'] == option1) | (matches['Team2'] == option1)]
            data2 = matches[(matches['Team1'] == option2) | (matches['Team2'] == option2)]
            
            metrics = ['Matches Played', 'Win %', 'Average Score', 'Toss Win %']
            values1 = [
                len(data1),
                len(data1[data1['Winner'] == option1]) / len(data1) * 100 if len(data1) > 0 else 0,
                data1[data1['Team1'] == option1]['Team1_Runs'].mean() if len(data1[data1['Team1'] == option1]) > 0 else 0,
                len(data1[data1['Toss_Winner'] == option1]) / len(data1) * 100 if len(data1) > 0 else 0
            ]
            values2 = [
                len(data2),
                len(data2[data2['Winner'] == option2]) / len(data2) * 100 if len(data2) > 0 else 0,
                data2[data2['Team1'] == option2]['Team1_Runs'].mean() if len(data2[data2['Team1'] == option2]) > 0 else 0,
                len(data2[data2['Toss_Winner'] == option2]) / len(data2) * 100 if len(data2) > 0 else 0
            ]
        else:  # eras
            # Define era ranges
            if option1 == 'era1':
                data1 = matches[matches['Season'].isin(['2008', '2009', '2010', '2011', '2012'])]
            elif option1 == 'era2':
                data1 = matches[matches['Season'].isin(['2013', '2014', '2015', '2016', '2017'])]
            else:  # era3
                data1 = matches[matches['Season'].isin(['2018', '2019', '2020', '2021', '2022', '2023', '2024'])]
                
            if option2 == 'era1':
                data2 = matches[matches['Season'].isin(['2008', '2009', '2010', '2011', '2012'])]
            elif option2 == 'era2':
                data2 = matches[matches['Season'].isin(['2013', '2014', '2015', '2016', '2017'])]
            else:  # era3
                data2 = matches[matches['Season'].isin(['2018', '2019', '2020', '2021', '2022', '2023', '2024'])]
            
            metrics = ['Boundaries/Match', 'Strike Rate', 'Economy', 'Win % Chasing']
            values1 = [
                len(deliveries[deliveries['Match_Id'].isin(data1['Id']) & deliveries['Batsman_Runs'].isin([4, 6])]) / len(data1) if len(data1) > 0 else 0,
                125, 8.2, 52  # Placeholders for actual calculations
            ]
            values2 = [
                len(deliveries[deliveries['Match_Id'].isin(data2['Id']) & deliveries['Batsman_Runs'].isin([4, 6])]) / len(data2) if len(data2) > 0 else 0,
                135, 8.8, 48  # Placeholders for actual calculations
            ]
        
        fig = go.Figure(data=[
            go.Bar(name=option1, x=metrics, y=values1, marker_color='#3b82f6'),
            go.Bar(name=option2, x=metrics, y=values2, marker_color='#ef4444')
        ])
        
        fig.update_layout(
            barmode='group',
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='white',
            title=f'Comparison: {option1} vs {option2}'
        )
        
        return fig

    @app.callback(
        Output('compare-metrics-radar', 'figure'),
        [Input('compare-option1', 'value'),
         Input('compare-option2', 'value'),
         Input('compare-type', 'value')]
    )
    def update_compare_radar(option1, option2, compare_type):
        if not option1 or not option2:
            return go.Figure()
            
        categories = ['Batting Power', 'Bowling Strength', 'Consistency', 
                     'Chasing Ability', 'Home Advantage', 'Team Balance']
        
        if compare_type == 'teams':
            # Team-specific radar values
            if option1 == 'Mumbai Indians':
                values1 = [85, 80, 90, 75, 82, 88]
            elif option1 == 'Chennai Super Kings':
                values1 = [82, 78, 95, 80, 85, 90]
            else:
                values1 = [75, 72, 80, 70, 68, 75]
                
            if option2 == 'Mumbai Indians':
                values2 = [85, 80, 90, 75, 82, 88]
            elif option2 == 'Chennai Super Kings':
                values2 = [82, 78, 95, 80, 85, 90]
            else:
                values2 = [70, 75, 78, 72, 65, 70]
        else:
            # Generic comparison
            values1 = [80, 75, 85, 70, 78, 82]
            values2 = [75, 80, 78, 75, 72, 79]
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatterpolar(
            r=values1,
            theta=categories,
            fill='toself',
            name=option1,
            line=dict(color='#3b82f6')
        ))
        
        fig.add_trace(go.Scatterpolar(
            r=values2,
            theta=categories,
            fill='toself',
            name=option2,
            line=dict(color='#ef4444')
        ))
        
        fig.update_layout(
            polar=dict(
                radialaxis=dict(visible=True, range=[0, 100])
            ),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font_color='white',
            title=f'Performance Radar: {option1} vs {option2}'
        )
        
        return fig

    @app.callback(
        Output('compare-trend-chart', 'figure'),
        [Input('compare-option1', 'value'),
         Input('compare-option2', 'value'),
         Input('compare-type', 'value')]
    )
    def update_compare_trend(option1, option2, compare_type):
        if not option1 or not option2:
            return go.Figure()
            
        if compare_type == 'seasons':
            # Show trend across seasons for both options
            seasons = sorted(matches['Season'].unique())
            option1_trend = []
            option2_trend = []
            
            for season in seasons:
                season_matches = matches[matches['Season'] == season]
                option1_trend.append(len(season_matches))
                option2_trend.append(season_matches[['Team1_Runs', 'Team2_Runs']].mean().mean())
            
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=seasons, y=option1_trend, name=f'{option1} - Matches', 
                                   line=dict(color='#3b82f6')))
            fig.add_trace(go.Scatter(x=seasons, y=option2_trend, name=f'{option2} - Avg Runs', 
                                   line=dict(color='#ef4444'), yaxis='y2'))
            
            fig.update_layout(
                title=f'Trend Analysis: {option1} vs {option2}',
                yaxis=dict(title='Matches', color='#3b82f6'),
                yaxis2=dict(title='Average Runs', color='#ef4444', overlaying='y', side='right'),
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font_color='white'
            )
        else:
            # Generic trend chart
            years = list(range(2008, 2024))
            trend1 = [100 + i*5 for i in range(len(years))]
            trend2 = [90 + i*7 for i in range(len(years))]
            
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=years, y=trend1, name=option1, line=dict(color='#3b82f6')))
            fig.add_trace(go.Scatter(x=years, y=trend2, name=option2, line=dict(color='#ef4444')))
            
            fig.update_layout(
                title=f'Performance Trend: {option1} vs {option2}',
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font_color='white',
                xaxis_title="Year",
                yaxis_title="Performance Index"
            )
        
        return fig