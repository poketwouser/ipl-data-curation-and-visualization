# ml/predict_winner.py
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
import warnings
warnings.filterwarnings('ignore')

class IPLWinPredictor:
    def __init__(self):
        self.model = None
        self.team_encoder = LabelEncoder()
        self.venue_encoder = LabelEncoder()
        self.is_trained = False
        
    def train_model(self, matches, deliveries):
        """Train the win prediction model"""
        print("Training IPL Win Prediction Model...")
        
        try:
            # Feature engineering
            features = self._engineer_features(matches, deliveries)
            
            if len(features) < 10:
                print("Insufficient data for training. Using rule-based approach.")
                self.is_trained = False
                return
            
            # Prepare features and target
            X = features.drop(['Winner', 'Match_Id'], axis=1, errors='ignore')
            y = features['Winner']
            
            # Encode categorical variables
            categorical_cols = ['Team1', 'Team2', 'Venue', 'Toss_Winner', 'Toss_Decision']
            for col in categorical_cols:
                if col in X.columns:
                    X[col] = X[col].astype(str)
            
            # Split data
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
            
            # Train model
            self.model = RandomForestClassifier(n_estimators=100, random_state=42, max_depth=10)
            self.model.fit(X_train, y_train)
            
            # Calculate training accuracy
            train_accuracy = self.model.score(X_train, y_train)
            test_accuracy = self.model.score(X_test, y_test)
            
            print(f"Model trained successfully!")
            print(f"Training Accuracy: {train_accuracy:.3f}")
            print(f"Test Accuracy: {test_accuracy:.3f}")
            self.is_trained = True
            
        except Exception as e:
            print(f"Model training failed: {e}")
            print("Using rule-based prediction as fallback")
            self.is_trained = False
    
    def _engineer_features(self, matches, deliveries):
        """Engineer features for the prediction model"""
        features_list = []
        
        for _, match in matches.iterrows():
            if pd.isna(match['Winner']) or match['Winner'] == 'No Result':
                continue
                
            # Basic match features
            features = {
                'Match_Id': match['Id'],
                'Team1': match['Team1'],
                'Team2': match['Team2'],
                'Venue': match['Venue'],
                'Toss_Winner': match['Toss_Winner'],
                'Toss_Decision': match['Toss_Decision'],
                'Winner': match['Winner']
            }
            
            # Calculate team form (last 5 matches)
            features.update(self._get_team_form(match, matches))
            
            # Calculate head-to-head record
            features.update(self._get_head_to_head(match, matches))
            
            # Calculate venue performance
            features.update(self._get_venue_stats(match, matches))
            
            features_list.append(features)
        
        return pd.DataFrame(features_list)
    
    def _get_team_form(self, match, matches):
        """Calculate team form based on recent matches"""
        form_features = {}
        
        for team in [match['Team1'], match['Team2']]:
            team_matches = matches[
                ((matches['Team1'] == team) | (matches['Team2'] == team)) &
                (matches['Date'] < match['Date'])
            ].tail(5)
            
            if len(team_matches) > 0:
                wins = len(team_matches[team_matches['Winner'] == team])
                form = wins / len(team_matches)
            else:
                form = 0.5  # Neutral form for no history
            
            form_features[f'{team}_form'] = form
        
        return form_features
    
    def _get_head_to_head(self, match, matches):
        """Calculate head-to-head statistics"""
        h2h_matches = matches[
            ((matches['Team1'] == match['Team1']) & (matches['Team2'] == match['Team2'])) |
            ((matches['Team1'] == match['Team2']) & (matches['Team2'] == match['Team1']))
        ]
        
        h2h_matches = h2h_matches[h2h_matches['Date'] < match['Date']]  # Only previous matches
        
        if len(h2h_matches) > 0:
            team1_wins = len(h2h_matches[h2h_matches['Winner'] == match['Team1']])
            team2_wins = len(h2h_matches[h2h_matches['Winner'] == match['Team2']])
            total_matches = len(h2h_matches)
            
            h2h_team1 = team1_wins / total_matches if total_matches > 0 else 0.5
            h2h_team2 = team2_wins / total_matches if total_matches > 0 else 0.5
        else:
            h2h_team1 = 0.5
            h2h_team2 = 0.5
        
        return {
            f"{match['Team1']}_h2h": h2h_team1,
            f"{match['Team2']}_h2h": h2h_team2
        }
    
    def _get_venue_stats(self, match, matches):
        """Calculate venue-specific statistics"""
        venue_matches = matches[matches['Venue'] == match['Venue']]
        venue_matches = venue_matches[venue_matches['Date'] < match['Date']]  # Only previous matches
        
        venue_features = {}
        
        for team in [match['Team1'], match['Team2']]:
            team_venue_matches = venue_matches[
                (venue_matches['Team1'] == team) | (venue_matches['Team2'] == team)
            ]
            
            if len(team_venue_matches) > 0:
                wins = len(team_venue_matches[team_venue_matches['Winner'] == team])
                venue_win_pct = wins / len(team_venue_matches)
            else:
                venue_win_pct = 0.5  # Neutral for no venue history
            
            venue_features[f'{team}_venue_win_pct'] = venue_win_pct
        
        return venue_features
    
    def predict_win_probability(self, team1, team2, venue):
        """Predict win probability for two teams at a venue"""
        if not self.is_trained:
            # Fallback to rule-based prediction
            return self._rule_based_prediction(team1, team2, venue)
        
        try:
            # Create feature vector for prediction
            features = self._create_prediction_features(team1, team2, venue)
            
            if features is None:
                return self._rule_based_prediction(team1, team2, venue)
            
            # Get probabilities
            probabilities = self.model.predict_proba([features])[0]
            classes = self.model.classes_
            
            # Find probabilities for each team
            team1_prob = 0
            team2_prob = 0
            
            for i, class_name in enumerate(classes):
                if class_name == team1:
                    team1_prob = probabilities[i] * 100
                elif class_name == team2:
                    team2_prob = probabilities[i] * 100
            
            # Normalize if needed
            total = team1_prob + team2_prob
            if total > 0:
                team1_prob = (team1_prob / total) * 100
                team2_prob = (team2_prob / total) * 100
            else:
                team1_prob = team2_prob = 50
            
            return team1_prob, team2_prob
            
        except Exception as e:
            print(f"ML prediction failed: {e}")
            return self._rule_based_prediction(team1, team2, venue)
    
    def _create_prediction_features(self, team1, team2, venue):
        """Create feature vector for prediction"""
        # This would need to be implemented based on the trained features
        # For now, return None to use rule-based approach
        return None
    
    def _rule_based_prediction(self, team1, team2, venue):
        """Rule-based prediction as fallback"""
        # Head-to-head record
        h2h_matches = matches[
            ((matches['Team1'] == team1) & (matches['Team2'] == team2)) |
            ((matches['Team1'] == team2) & (matches['Team2'] == team1))
        ]
        
        if len(h2h_matches) > 0:
            team1_wins = len(h2h_matches[h2h_matches['Winner'] == team1])
            team2_wins = len(h2h_matches[h2h_matches['Winner'] == team2])
            total_matches = team1_wins + team2_wins
            
            if total_matches > 0:
                team1_prob = (team1_wins / total_matches) * 100
                team2_prob = (team2_wins / total_matches) * 100
            else:
                team1_prob = team2_prob = 50
        else:
            team1_prob = team2_prob = 50
        
        # Adjust based on venue performance
        venue_matches = matches[matches['Venue'] == venue]
        if len(venue_matches) > 0:
            team1_venue_wins = len(venue_matches[venue_matches['Winner'] == team1])
            team2_venue_wins = len(venue_matches[venue_matches['Winner'] == team2])
            total_venue_matches = team1_venue_wins + team2_venue_wins
            
            if total_venue_matches > 0:
                venue_impact = 0.2  # 20% weight to venue performance
                team1_venue_adj = (team1_venue_wins / total_venue_matches) * venue_impact * 100
                team2_venue_adj = (team2_venue_wins / total_venue_matches) * venue_impact * 100
                
                team1_prob = team1_prob * (1 - venue_impact) + team1_venue_adj
                team2_prob = team2_prob * (1 - venue_impact) + team2_venue_adj
        
        # Ensure probabilities sum to 100
        total = team1_prob + team2_prob
        if total > 0:
            team1_prob = (team1_prob / total) * 100
            team2_prob = (team2_prob / total) * 100
        
        return team1_prob, team2_prob