import os
import sys
import json
import yaml
import time
import pandas as pd
from pathlib import Path
from yfpy import YahooFantasySportsQuery

# allow imports from utils.py in parent directory
# Add the parent directory to the Python path
parent_dir = project_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
print(parent_dir)
sys.path.insert(0, parent_dir)
from utils import get_yaml

def get_season_scores(secrets_path, league_id, game_code, game_id, season):
    # accumulate season results
    lids = []
    gids = []
    szns = []
    wks = []
    tm1_ids = []
    tm1_nms = []
    tm1_proj = []
    tm1_act = []
    tm2_ids = []
    tm2_nms = []
    tm2_proj = []
    tm2_act = []

    # initialize Yahoo Query for this season
    query = YahooFantasySportsQuery(auth_dir=secrets_path,
                                    league_id=league_id,
                                    game_code=game_code,
                                    game_id=game_id,
                                    browser_callback=False)
    
    # get list of all fantasy weeks
    # Seasons 2010-2020: 16 weeks
    # Seasons 2021-present: 17 weeks
    game = query.get_current_game_info()
    game_weeks = game.game_weeks

    if season < 2021:
        weeks = [gw.week for gw in game_weeks if gw.week <= 16]
    else:
        weeks = [gw.week for gw in game_weeks if gw.week <= 17]

    # grab scoreboard for each week in the season
    for wk in weeks:
        # giving it a pause between calls
        # had remote disconnect before
        time.sleep(10)

        print("Week #: {}".format(wk))
        scoreboard = query.get_league_scoreboard_by_week(wk)
        matchups = scoreboard.matchups
        # extract predicted and actual scores for each matchup
        for matchup in matchups:
            teams = matchup.teams
            # for both teams we need
            # projected points and actual points
            team1 = teams[0]
            team2 = teams[1]

            team1_name = team1.name
            team1_id = team1.team_id
            team1_points = team1.team_points.total
            team1_projected = team1.team_projected_points.total

            team2_name = team2.name
            team2_id = team2.team_id
            team2_points = team2.team_points.total
            team2_projected = team2.team_projected_points.total

            # append values to lists
            lids.append(league_id)
            gids.append(game_id)
            szns.append(season)
            wks.append(wk)
            tm1_ids.append(team1_id)
            tm1_nms.append(team1_name)
            tm1_act.append(team1_points)
            tm1_proj.append(team1_projected)
            tm2_ids.append(team2_id)
            tm2_nms.append(team2_name)
            tm2_act.append(team2_points)
            tm2_proj.append(team2_projected)

    # create dataframe from lists
    game_results = pd.DataFrame({'league_id': lids,
                                 'game_id': gids,
                                 'season': szns,
                                 'week': wks,
                                 'away_team_id': tm1_ids,
                                 'away_team_name': tm1_nms,
                                 'away_team_projected': tm1_proj,
                                 'away_team_actual': tm1_act,
                                 'home_team_id': tm2_ids,
                                 'home_team_name': tm2_nms,
                                 'home_team_projected': tm2_proj,
                                 'home_team_actual': tm2_act})

    return game_results

def main():
    # read in config
    # Path to the directory where the current script is located
    current_script_dir = os.path.dirname(os.path.abspath(__file__))
    # Path to the 'backend_config.yml' file relative to the current script
    config_file_path = os.path.join(current_script_dir, 'backend_config.yml')
    config = get_yaml(config_file_path)

    private_json_path = Path(config["secrets_path"])
    game_code = config["game_code"]
    game_ids = config['games']

    results_df = pd.DataFrame(columns=['league_id', 'game_id', 'season', 'week',
                                       'away_team_id', 'away_team_name', 'away_team_projected', 'away_team_actual',
                                       'home_team_id', 'home_team_name', 'home_team_projected', 'home_team_actual'])
    # for each game_id
    for game_id, league_info in game_ids.items():
        game_id = str(game_id)
        # for each league season
        for league_id, season in league_info.items():
            league_id = str(league_id)
            print(season)
            print('')
            
            matchup_results = get_season_scores(private_json_path, league_id, game_code, game_id, season)
            results_df = pd.concat([results_df, matchup_results], axis=0)
    
    # write output to disk
    data_path = os.path.join(current_script_dir, 'data/matchup_results.csv')
    results_df.to_csv(data_path, header=True, index=False)

if __name__ == '__main__':
    main()