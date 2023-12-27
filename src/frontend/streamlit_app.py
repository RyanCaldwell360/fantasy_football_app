import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import plotly.graph_objects as go

# include separate tabs
# standings
# playoff odds
# weekly matchups
tab1, tab2, tab3 = st.tabs(["Standings", "Playoffs", "Weekly Matchups"])

# matchup data
matchups = pd.read_csv('./src/backend/data_extraction/data/matchup_results.csv')

with tab1:
    st.header("Standings")

with tab2:
    st.header("Playoff Race")

with tab3:
    st.header("Weekly Matchups")
    # only show subset of columns
    matchup_condensed = matchups[['season','week','away_team_name','away_team_nickname','away_team_division_name',
                                  'away_team_actual','away_team_projected','home_team_name','home_team_nickname',
                                  'home_team_division_name','home_team_actual','home_team_projected']]
    matchup_condensed['season'] = matchup_condensed['season'].astype(str)

    # Get unique seasons and weeks for the selectbox options
    seasons = sorted(matchup_condensed['season'].unique())
    weeks = sorted(matchup_condensed['week'].unique())

    # Create selectboxes for season and week
    selected_season = st.selectbox('Select a Season', seasons)
    selected_week = st.selectbox('Select a Week', weeks)

    # Filter the dataframe based on the selected season and week
    filtered_matchups = matchup_condensed[(matchup_condensed['season'] == selected_season) & 
                                          (matchup_condensed['week'] == selected_week)]
    # write table to screen
    # st.table(filtered_matchups.reset_index(drop=True))

    # Create a figure
    fig = go.Figure()

    # Create x-axis labels
    x_labels = filtered_matchups['away_team_name'] + '<br>' + filtered_matchups['home_team_name']

    # Loop over each matchup
    for i in range(len(x_labels)):
        # Add traces for projected and actual scores for away team
        fig.add_trace(go.Scatter(x=[i - 0.1, i - 0.1], y=[filtered_matchups['away_team_projected'].iloc[i], filtered_matchups['away_team_actual'].iloc[i]], mode='markers+lines', name='Away Team' if i == 0 else '', legendgroup='Away Team', line=dict(color='blue', dash='dash'), customdata=[[filtered_matchups['away_team_name'].iloc[i], filtered_matchups['away_team_projected'].iloc[i], filtered_matchups['away_team_actual'].iloc[i]]]*2, hovertemplate='Team: %{customdata[0]}<br>Projected: %{customdata[1]}<br>Actual: %{customdata[2]}', showlegend=False if i > 0 else True))

        # Add arrow for away team
        fig.add_annotation(x=i - 0.1, y=filtered_matchups['away_team_actual'].iloc[i], ax=i - 0.1, ay=filtered_matchups['away_team_projected'].iloc[i], arrowhead=1, arrowsize=1, arrowwidth=2, arrowcolor='blue', axref="x", ayref="y")

        # Add traces for projected and actual scores for home team
        fig.add_trace(go.Scatter(x=[i + 0.1, i + 0.1], y=[filtered_matchups['home_team_projected'].iloc[i], filtered_matchups['home_team_actual'].iloc[i]], mode='markers+lines', name='Home Team' if i == 0 else '', legendgroup='Home Team', line=dict(color='red', dash='dash'), customdata=[[filtered_matchups['home_team_name'].iloc[i], filtered_matchups['home_team_projected'].iloc[i], filtered_matchups['home_team_actual'].iloc[i]]]*2, hovertemplate='Team: %{customdata[0]}<br>Projected: %{customdata[1]}<br>Actual: %{customdata[2]}', showlegend=False if i > 0 else True))

        # Add arrow for home team
        fig.add_annotation(x=i + 0.1, y=filtered_matchups['home_team_actual'].iloc[i], ax=i + 0.1, ay=filtered_matchups['home_team_projected'].iloc[i], arrowhead=1, arrowsize=1, arrowwidth=2, arrowcolor='red', axref="x", ayref="y")
    
    # Update layout
    fig.update_layout(xaxis=dict(showticklabels=True, tickangle=0), yaxis_title='Score', title='Projected vs Actual Scores')

    # Set x-axis tick labels
    fig.update_xaxes(tickvals=list(range(len(x_labels))), ticktext=x_labels)

    # Display the figure
    st.plotly_chart(fig)