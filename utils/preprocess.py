# utils/preprocess.py
import pandas as pd
import numpy as np

def preprocess_matches_data(matches_df):
    """Preprocess matches data for analytics"""
    print("Preprocessing matches data...")
    
    # Create a copy to avoid modifying original
    matches = matches_df.copy()
    
    # Convert date and ensure proper types
    matches['Date'] = pd.to_datetime(matches['Date'])
    matches['Season'] = matches['Season'].astype(str)
    matches['Match_No'] = matches['Match_No'].astype(str)
    
    # Handle missing values
    matches['Winner'].fillna('No Result', inplace=True)
    matches['Result'].fillna('No Result', inplace=True)
    matches['Player_Of_Match'].fillna('Not Awarded', inplace=True)
    matches['Toss_Decision'].fillna('Unknown', inplace=True)
    
    # Calculate additional metrics
    matches['Total_Runs_In_Match'] = matches['Team1_Runs'] + matches['Team2_Runs']
    matches['Total_Wickets_In_Match'] = matches['Team1_Wickets'] + matches['Team2_Wickets']
    
    print(f"Preprocessed {len(matches)} matches")
    return matches

def preprocess_deliveries_data(deliveries_df):
    """Preprocess deliveries data for analytics"""
    print("Preprocessing deliveries data...")
    
    # Create a copy to avoid modifying original
    deliveries = deliveries_df.copy()
    
    # Handle missing values
    deliveries['Player_Dismissed'].fillna('', inplace=True)
    deliveries['Dismissal_Kind'].fillna('', inplace=True)
    deliveries['Fielder'].fillna('', inplace=True)
    deliveries['Extras_Type'].fillna('', inplace=True)
    
    # Ensure numeric columns are properly typed
    numeric_columns = ['Over', 'Ball', 'Batsman_Runs', 'Extra_Runs', 'Total_Runs', 'Is_Wicket']
    for col in numeric_columns:
        if col in deliveries.columns:
            deliveries[col] = pd.to_numeric(deliveries[col], errors='coerce').fillna(0)
    
    # Create additional features
    deliveries['Is_Boundary'] = deliveries['Batsman_Runs'].isin([4, 6])
    deliveries['Is_Six'] = (deliveries['Batsman_Runs'] == 6)
    deliveries['Is_Four'] = (deliveries['Batsman_Runs'] == 4)
    
    print(f"Preprocessed {len(deliveries)} deliveries")
    return deliveries

def calculate_player_stats(deliveries_df, matches_df):
    """Calculate comprehensive player statistics"""
    print("Calculating player statistics...")
    
    # Batting stats
    batting_stats = deliveries_df.groupby('Batter').agg({
        'Batsman_Runs': ['sum', 'mean', 'count'],
        'Match_Id': 'nunique',
        'Is_Wicket': 'sum',
        'Is_Boundary': 'sum',
        'Is_Six': 'sum',
        'Is_Four': 'sum'
    }).round(2)
    
    # Flatten column names
    batting_stats.columns = [
        'Total_Runs', 'Avg_Runs_Per_Ball', 'Balls_Faced', 
        'Matches', 'Times_Dismissed', 'Boundaries', 'Sixes', 'Fours'
    ]
    
    # Calculate derived stats
    batting_stats['Batting_Average'] = (
        batting_stats['Total_Runs'] / batting_stats['Times_Dismissed']
    ).replace([np.inf, -np.inf], batting_stats['Total_Runs'])
    
    batting_stats['Strike_Rate'] = (
        batting_stats['Total_Runs'] / batting_stats['Balls_Faced'] * 100
    ).replace([np.inf, -np.inf], 0)
    
    batting_stats['Boundary_Percentage'] = (
        batting_stats['Boundaries'] / batting_stats['Balls_Faced'] * 100
    ).replace([np.inf, -np.inf], 0)
    
    # Bowling stats (simplified)
    bowling_stats = deliveries_df[
        (deliveries_df['Is_Wicket'] == 1) & 
        (~deliveries_df['Dismissal_Kind'].isin(['Run Out', 'Obstructing The Field', 'Retired Hurt']))
    ].groupby('Bowler').agg({
        'Is_Wicket': 'count',
        'Total_Runs': 'sum',
        'Match_Id': 'nunique'
    }).round(2)
    
    bowling_stats.columns = ['Wickets', 'Runs_Conceded', 'Matches_Bowled']
    
    bowling_stats['Bowling_Average'] = (
        bowling_stats['Runs_Conceded'] / bowling_stats['Wickets']
    ).replace([np.inf, -np.inf], bowling_stats['Runs_Conceded'])
    
    # Merge batting and bowling stats
    player_stats = batting_stats.join(bowling_stats, how='outer')
    
    # Fill NaN values
    player_stats = player_stats.fillna(0)
    
    print(f"Calculated stats for {len(player_stats)} players")
    return player_stats

def calculate_advanced_metrics(deliveries_df, matches_df):
    """Calculate advanced cricket metrics"""
    print("Calculating advanced metrics...")
    
    # Match-level metrics
    match_metrics = matches_df.groupby('Season').agg({
        'Id': 'count',
        'Total_Runs_In_Match': 'mean',
        'Total_Wickets_In_Match': 'mean',
        'Super_Over': lambda x: (x == 'Y').sum()
    }).round(2)
    
    match_metrics.columns = ['Matches', 'Avg_Runs_Per_Match', 'Avg_Wickets_Per_Match', 'Super_Overs']
    
    # Player season performance
    season_performance = deliveries_df.merge(
        matches_df[['Id', 'Season']], 
        left_on='Match_Id', 
        right_on='Id'
    )
    
    player_season_stats = season_performance.groupby(['Batter', 'Season']).agg({
        'Batsman_Runs': 'sum',
        'Match_Id': 'nunique',
        'Is_Boundary': 'sum'
    }).reset_index()
    
    player_season_stats.columns = ['Player', 'Season', 'Runs', 'Matches', 'Boundaries']
    
    return {
        'match_metrics': match_metrics,
        'player_season_stats': player_season_stats
    }