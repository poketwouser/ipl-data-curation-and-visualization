# utils/aggregates.py
import pandas as pd
import numpy as np

def calculate_team_performance(matches_df, team_name):
    """Calculate comprehensive team performance metrics"""
    team_matches = matches_df[
        (matches_df['Team1'] == team_name) | 
        (matches_df['Team2'] == team_name)
    ]
    
    if len(team_matches) == 0:
        return None
    
    total_matches = len(team_matches)
    wins = len(team_matches[team_matches['Winner'] == team_name])
    losses = total_matches - wins
    
    # Calculate win percentage
    win_percentage = (wins / total_matches * 100) if total_matches > 0 else 0
    
    # Home vs Away performance
    home_matches = team_matches[team_matches['Team1'] == team_name]
    away_matches = team_matches[team_matches['Team2'] == team_name]
    
    home_wins = len(home_matches[home_matches['Winner'] == team_name])
    away_wins = len(away_matches[away_matches['Winner'] == team_name])
    
    home_win_pct = (home_wins / len(home_matches) * 100) if len(home_matches) > 0 else 0
    away_win_pct = (away_wins / len(away_matches) * 100) if len(away_matches) > 0 else 0
    
    # Toss impact
    toss_wins = len(team_matches[team_matches['Toss_Winner'] == team_name])
    toss_win_match_wins = len(team_matches[
        (team_matches['Toss_Winner'] == team_name) & 
        (team_matches['Winner'] == team_name)
    ])
    
    toss_impact = (toss_win_match_wins / toss_wins * 100) if toss_wins > 0 else 0
    
    return {
        'total_matches': total_matches,
        'wins': wins,
        'losses': losses,
        'win_percentage': win_percentage,
        'home_win_percentage': home_win_pct,
        'away_win_percentage': away_win_pct,
        'toss_impact': toss_impact,
        'home_matches': len(home_matches),
        'away_matches': len(away_matches)
    }

def calculate_venue_stats(matches_df, venue_name):
    """Calculate venue-specific statistics"""
    venue_matches = matches_df[matches_df['Venue'] == venue_name]
    
    if len(venue_matches) == 0:
        return None
    
    stats = {
        'total_matches': len(venue_matches),
        'avg_runs_per_match': venue_matches[['Team1_Runs', 'Team2_Runs']].mean().mean(),
        'avg_wickets_per_match': venue_matches[['Team1_Wickets', 'Team2_Wickets']].mean().mean(),
        'bat_first_wins': len(venue_matches[venue_matches['Toss_Decision'] == 'Bat']),
        'super_overs': len(venue_matches[venue_matches['Super_Over'] == 'Y'])
    }
    
    # Most successful team at venue
    if not venue_matches['Winner'].empty and pd.notna(venue_matches['Winner']).any():
        winner_counts = venue_matches['Winner'].value_counts()
        stats['most_successful_team'] = winner_counts.index[0]
        stats['most_successful_wins'] = winner_counts.iloc[0]
    else:
        stats['most_successful_team'] = 'N/A'
        stats['most_successful_wins'] = 0
    
    # Toss decision impact
    bat_first_wins = len(venue_matches[
        (venue_matches['Toss_Decision'] == 'Bat') & 
        (venue_matches['Toss_Winner'] == venue_matches['Winner'])
    ])
    
    field_first_wins = len(venue_matches[
        (venue_matches['Toss_Decision'] == 'Field') & 
        (venue_matches['Toss_Winner'] == venue_matches['Winner'])
    ])
    
    stats['bat_first_win_pct'] = (bat_first_wins / stats['bat_first_wins'] * 100) if stats['bat_first_wins'] > 0 else 0
    stats['field_first_win_pct'] = (field_first_wins / (len(venue_matches) - stats['bat_first_wins']) * 100) if (len(venue_matches) - stats['bat_first_wins']) > 0 else 0
    
    return stats

def calculate_player_vs_team_stats(deliveries_df, matches_df, player_name, team_name):
    """Calculate player performance against specific team"""
    player_vs_team = deliveries_df[
        (deliveries_df['Batter'] == player_name) & 
        (deliveries_df['Bowling_Team'] == team_name)
    ]
    
    if len(player_vs_team) == 0:
        return None
    
    # Basic stats
    total_runs = player_vs_team['Batsman_Runs'].sum()
    total_balls = len(player_vs_team[~player_vs_team['Extras_Type'].isin(['Wides', 'Noballs'])])
    strike_rate = (total_runs / total_balls * 100) if total_balls > 0 else 0
    
    # Dismissals
    dismissals = len(player_vs_team[
        (player_vs_team['Is_Wicket'] == 1) & 
        (player_vs_team['Player_Dismissed'] == player_name)
    ])
    
    average = total_runs / dismissals if dismissals > 0 else total_runs
    
    # Boundaries
    boundaries = len(player_vs_team[player_vs_team['Batsman_Runs'].isin([4, 6])])
    sixes = len(player_vs_team[player_vs_team['Batsman_Runs'] == 6])
    fours = len(player_vs_team[player_vs_team['Batsman_Runs'] == 4])
    
    # Match performance
    matches_played = player_vs_team['Match_Id'].nunique()
    best_score = player_vs_team.groupby('Match_Id')['Batsman_Runs'].sum().max()
    
    # Dismissal types
    dismissal_types = player_vs_team[
        (player_vs_team['Is_Wicket'] == 1) & 
        (player_vs_team['Player_Dismissed'] == player_name)
    ]['Dismissal_Kind'].value_counts().to_dict()
    
    return {
        'total_runs': total_runs,
        'matches_played': matches_played,
        'innings': player_vs_team['Inning'].nunique(),
        'average': average,
        'strike_rate': strike_rate,
        'best_score': best_score,
        'boundaries': boundaries,
        'sixes': sixes,
        'fours': fours,
        'dismissals': dismissals,
        'dismissal_types': dismissal_types,
        'balls_faced': total_balls
    }

def calculate_season_summary(matches_df, deliveries_df, season):
    """Calculate comprehensive season summary"""
    season_matches = matches_df[matches_df['Season'] == season]
    
    if len(season_matches) == 0:
        return None
    
    season_match_ids = season_matches['Id'].tolist()
    season_deliveries = deliveries_df[deliveries_df['Match_Id'].isin(season_match_ids)]
    
    # Basic season stats
    summary = {
        'total_matches': len(season_matches),
        'super_overs': len(season_matches[season_matches['Super_Over'] == 'Y']),
        'avg_runs_per_match': season_matches[['Team1_Runs', 'Team2_Runs']].mean().mean(),
        'avg_wickets_per_match': season_matches[['Team1_Wickets', 'Team2_Wickets']].mean().mean(),
        'champion': season_matches[season_matches['Match_Type'] == 'Final']['Winner'].iloc[0] 
                   if not season_matches[season_matches['Match_Type'] == 'Final'].empty else 'N/A'
    }
    
    # Boundary analysis
    boundaries = season_deliveries[season_deliveries['Batsman_Runs'].isin([4, 6])]
    summary['total_boundaries'] = len(boundaries)
    summary['total_sixes'] = len(season_deliveries[season_deliveries['Batsman_Runs'] == 6])
    summary['total_fours'] = len(season_deliveries[season_deliveries['Batsman_Runs'] == 4])
    summary['boundaries_per_match'] = summary['total_boundaries'] / summary['total_matches']
    
    # Toss analysis
    toss_winners = season_matches[season_matches['Toss_Winner'] == season_matches['Winner']]
    summary['toss_win_impact'] = len(toss_winners) / len(season_matches) * 100
    
    return summary