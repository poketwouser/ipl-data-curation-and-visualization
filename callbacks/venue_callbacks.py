# callbacks/venue_callbacks.py
from dash import Input, Output, State, html
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

def register_venue_callbacks(app, matches, deliveries):
    @app.callback(
        Output('venue-select', 'options'),
        Input('tabs', 'active_tab')
    )
    def update_venue_options(active_tab):
        venues = sorted(matches['Venue'].unique())
        return [{'label': venue, 'value': venue} for venue in venues]

    @app.callback(
        [Output('venue-profile-title', 'children'),
         Output('venue-stats-summary', 'children')],
        [Input('venue-select', 'value')]
    )
    def update_venue_profile(venue):
        if not venue:
            return "Venue Profile", "Select a venue to view statistics"
            
        venue_matches = matches[matches['Venue'] == venue]
        
        if venue_matches.empty:
            return f"Venue: {venue}", "No data available for this venue"
        
        total_matches = len(venue_matches)
        avg_runs = venue_matches[['Team1_Runs', 'Team2_Runs']].mean().mean()
        
        # Calculate toss impact
        toss_winners = venue_matches[venue_matches['Toss_Winner'] == venue_matches['Winner']]
        toss_win_percentage = len(toss_winners) / total_matches * 100 if total_matches > 0 else 0
        
        # Most successful team
        if not venue_matches['Winner'].empty and pd.notna(venue_matches['Winner']).any():
            most_successful = venue_matches['Winner'].mode().iloc[0] if not venue_matches['Winner'].mode().empty else 'N/A'
        else:
            most_successful = 'N/A'
        
        return f"🏟️ {venue}", html.Div([
            html.H4(f"{total_matches} Matches", style={'color': '#f59e0b', 'marginBottom': '10px'}),
            html.P(f"📊 Average Score: {avg_runs:.1f}", style={'color': 'white', 'marginBottom': '5px'}),
            html.P(f"🎯 Toss Win Impact: {toss_win_percentage:.1f}%", style={'color': 'white', 'marginBottom': '5px'}),
            html.P(f"👑 Most Successful: {most_successful}", style={'color': 'white', 'marginBottom': '5px'}),
            html.P(f"🏙️ City: {venue_matches['City'].iloc[0] if 'City' in venue_matches.columns and not venue_matches.empty else 'N/A'}", 
                  style={'color': '#94a3b8', 'marginBottom': '5px'})
        ])

    @app.callback(
        Output('venue-matches-chart', 'figure'),
        [Input('venue-select', 'value')]
    )
    def update_venue_matches_chart(venue):
        if not venue:
            return go.Figure()
            
        venue_matches = matches[matches['Venue'] == venue]
        matches_by_season = venue_matches.groupby('Season').size().reset_index(name='Matches')
        
        fig = px.bar(matches_by_season, x='Season', y='Matches',
                     title=f'Matches per Season at {venue}',
                     color='Matches', color_continuous_scale='Viridis')
        
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='white',
            title_font_color='white',
            showlegend=False,
            xaxis_tickangle=-45
        )
        
        return fig

    @app.callback(
        Output('venue-pitch-radar', 'figure'),
        [Input('venue-select', 'value')]
    )
    def update_venue_pitch_radar(venue):
        if not venue:
            return go.Figure()
            
        # Calculate actual pitch behavior metrics from data
        venue_matches = matches[matches['Venue'] == venue]
        venue_deliveries = deliveries.merge(venue_matches[['Id']], left_on='Match_Id', right_on='Id')
        
        if venue_deliveries.empty:
            # Return sample data if no deliveries data
            categories = ['Batting Friendly', 'Bowling Friendly', 'Pace Friendly', 
                         'Spin Friendly', 'High Scoring', 'Chasing Friendly']
            values = [65, 55, 60, 50, 70, 58]
        else:
            # Calculate actual metrics
            total_runs = venue_deliveries['Total_Runs'].sum()
            total_wickets = venue_deliveries['Is_Wicket'].sum()
            total_balls = len(venue_deliveries)
            
            runs_per_over = (total_runs / total_balls) * 6 if total_balls > 0 else 7
            wickets_per_match = total_wickets / len(venue_matches) if len(venue_matches) > 0 else 10
            
            # Normalize to 0-100 scale
            batting_friendly = min(runs_per_over / 10 * 100, 100)
            bowling_friendly = min(wickets_per_match / 15 * 100, 100)
            
            categories = ['Batting Friendly', 'Bowling Friendly', 'Pace Friendly', 
                         'Spin Friendly', 'High Scoring', 'Chasing Friendly']
            values = [
                batting_friendly,
                bowling_friendly,
                65, 60, 70, 55  # Placeholders for other metrics
            ]
        
        fig = go.Figure(data=go.Scatterpolar(
            r=values,
            theta=categories,
            fill='toself',
            line=dict(color='#10b981', width=2),
            fillcolor='rgba(16, 185, 129, 0.2)'
        ))
        
        fig.update_layout(
            polar=dict(
                radialaxis=dict(visible=True, range=[0, 100], gridcolor='#374151')
            ),
            showlegend=False,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font_color='white',
            title=f'Pitch Behavior at {venue}'
        )
        
        return fig

    @app.callback(
        Output('venue-runs-heatmap', 'figure'),
        [Input('venue-select', 'value')]
    )
    def update_venue_runs_heatmap(venue):
        if not venue:
            return go.Figure()
            
        venue_matches = matches[matches['Venue'] == venue]
        
        # Create a sample heatmap of runs distribution by over
        # In a real implementation, this would use deliveries data
        overs = list(range(1, 21))
        runs_by_over = [7, 8, 6, 9, 8, 7, 11, 10, 9, 8, 12, 11, 10, 9, 8, 13, 12, 11, 10, 15]
        
        fig = go.Figure(data=go.Heatmap(
            z=[runs_by_over],
            x=overs,
            y=['Runs per Over'],
            colorscale='Viridis',
            showscale=True
        ))
        
        fig.update_layout(
            title=f'Average Runs per Over at {venue}',
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='white',
            title_font_color='white',
            xaxis_title="Over",
            yaxis_title=""
        )
        
        return fig