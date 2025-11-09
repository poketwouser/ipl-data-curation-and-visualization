# components/navigation.py
import dash_bootstrap_components as dbc

def create_navigation():
    return dbc.Tabs([
        dbc.Tab(label="🏆 Season Overview", tab_id="season"),
        dbc.Tab(label="📊 Match Explorer", tab_id="match"),
        dbc.Tab(label="👤 Player Intelligence", tab_id="player"),
        dbc.Tab(label="⚔️ Player vs Player", tab_id="pvp"),
        dbc.Tab(label="🎯 Player vs Team", tab_id="pvt"),
        dbc.Tab(label="🏟️ Venue Insights", tab_id="venue"),
        dbc.Tab(label="📈 Compare Analytics", tab_id="compare"),
        dbc.Tab(label="🤖 AI Predictions", tab_id="ml"),
        dbc.Tab(label="🌟 Dream XI Builder", tab_id="dreamxi"),
        dbc.Tab(label="📊 All-Time Records", tab_id="records"),
    ], id="tabs", active_tab="season", className="mb-4")