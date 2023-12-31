import os
import sys
import boto3
import pandas as pd
import streamlit as st
import plotly.graph_objects as go

# allow imports from utils.py in parent directory
# Add the parent directory to the Python path
parent_dir = project_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, parent_dir)
from utils import get_yaml

# read in config
config_file_path = 'src/backend/data_extraction/backend_config.yml'
config = get_yaml(config_file_path)

# AWS credentials
aws_access_key_id = st.secrets["aws"]["aws_access_key_id"]
aws_secret_access_key = st.secrets["aws"]["aws_secret_access_key"]

# permissions
session = boto3.Session(aws_access_key_id=aws_access_key_id,
                        aws_secret_access_key=aws_secret_access_key)

# Use the session to interact with S3
s3 = session.resource('s3')

# Now you can perform operations on this bucket
bucket_name = config['file_paths']['bucket_name']
bucket = s3.Bucket(bucket_name)

# include separate tabs
# standings
# playoff odds
# weekly matchups
tab1, tab2, tab3 = st.tabs(["Standings", "Playoffs", "Weekly Matchups"])

# matchup data
matchup_path = 's3://' + bucket_name + config['file_paths']['matchup'] + '/matchup_results.csv'
matchups = pd.read_csv(matchup_path, 
                       storage_options={'key': aws_access_key_id, 
                                        'secret': aws_secret_access_key})

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