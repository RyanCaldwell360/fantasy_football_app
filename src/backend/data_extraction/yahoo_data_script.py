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

def get_season_matchups(secrets_path, league_id, game_code, game_id, season):
    # accumulate season results
    lids = []
    gids = []
    szns = []
    wks = []
    # team 1 data
    tm1_ids = []
    tm1_mid = []
    tm1_nms = []
    tm1_nkn = []
    tm1_div = []
    tm1_act = []
    tm1_proj = []
    # team 2 data
    tm2_ids = []
    tm2_mid = []
    tm2_nms = []
    tm2_nkn = []
    tm2_div = []
    tm2_act = []
    tm2_proj = []

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
        # time.sleep(3)

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

            team1_manager = team1.managers[0]
            team2_manager = team2.managers[0]

            team1_id = team1.team_id
            team1_manager_id = team1_manager.manager_id
            team1_name = team1.name.decode('utf-8')
            team1_nickname = team1_manager.nickname
            team1_division_id = team1.division_id
            team1_points = team1.team_points.total
            team1_projected = team1.team_projected_points.total

            team2_id = team2.team_id
            team2_manager_id = team2_manager.manager_id
            team2_name = team2.name.decode('utf-8')
            team2_nickname = team2_manager.nickname
            team2_division_id = team2.division_id
            team2_points = team2.team_points.total
            team2_projected = team2.team_projected_points.total

            # append values to lists
            lids.append(league_id)
            gids.append(game_id)
            szns.append(season)
            wks.append(wk)
            # team 1
            tm1_ids.append(team1_id)
            tm1_mid.append(team1_manager_id)
            tm1_nms.append(team1_name)
            tm1_nkn.append(team1_nickname)
            tm1_div.append(team1_division_id)
            tm1_act.append(team1_points)
            tm1_proj.append(team1_projected)
            # team 2
            tm2_ids.append(team2_id)
            tm2_mid.append(team2_manager_id)
            tm2_nms.append(team2_name)
            tm2_nkn.append(team2_nickname)
            tm2_div.append(team2_division_id)
            tm2_act.append(team2_points)
            tm2_proj.append(team2_projected)

    # create dataframe from lists
    game_results = pd.DataFrame({'league_id': lids,
                                 'game_id': gids,
                                 'season': szns,
                                 'week': wks,
                                 'away_team_id': tm1_ids,
                                 'away_team_manager_id': tm1_mid,
                                 'away_team_name': tm1_nms,
                                 'away_team_nickname': tm1_nkn,
                                 'away_team_division_id': tm1_div,
                                 'away_team_actual': tm1_act,
                                 'away_team_projected': tm1_proj,
                                 'home_team_id': tm2_ids,
                                 'home_team_manager_id': tm2_mid,
                                 'home_team_name': tm2_nms,
                                 'home_team_nickname': tm2_nkn,
                                 'home_team_division_id': tm2_div,
                                 'home_team_actual': tm2_act,
                                 'home_team_projected': tm2_proj})

    return game_results

def get_all_season_matchups(private_json_path, game_code, game_ids):
    results_df = pd.DataFrame(columns=['league_id', 'game_id', 'season', 'week',
                                       'away_team_id', 'away_team_manager_id', 'away_team_name', 'away_team_nickname', 
                                       'away_team_division_id', 'away_team_actual', 'away_team_projected',
                                       'home_team_id', 'home_team_manager_id', 'home_team_name', 'home_team_nickname', 
                                       'home_team_division_id', 'home_team_actual', 'home_team_projected'])
    # for each game_id
    for game_id, league_info in game_ids.items():
        game_id = str(game_id)
        # for each league season
        for league_id, season in league_info.items():
            league_id = str(league_id)
            print(season)
            print('')
            
            matchup_results = get_season_matchups(private_json_path, league_id, game_code, game_id, season)
            results_df = pd.concat([results_df, matchup_results], axis=0)

    results_df = results_df.reset_index(drop=True)

    return results_df

def get_divisions(private_json_path, game_code, game_ids):
    division_df = pd.DataFrame(columns=['league_id', 'game_id', 'season', 'division_id', 'division_name'])
    # for each game_id
    for game_id, league_info in game_ids.items():
        game_id = str(game_id)
        # for each league season
        for league_id, season in league_info.items():
            league_id = str(league_id)

            # extract division info from league settings
            query = YahooFantasySportsQuery(private_json_path, league_id, 'nfl', game_id)
            settings = query.get_league_settings()
            # temp holder
            for d in settings.divisions:
                temp = pd.DataFrame({'league_id':[league_id],
                                     'game_id':[game_id],
                                     'season':[season],
                                     'division_id':[d.division_id],
                                     'division_name':[d.name]})
                division_df = pd.concat([division_df, temp], axis=0)

    division_df = division_df.reset_index(drop=True)

    return division_df

def combine_matchups_divisions(matchup_results, divisions):
    results_df = matchup_results.merge(divisions, how='left', 
                                       left_on=['league_id','game_id','season','away_team_division_id'], 
                                       right_on=['league_id','game_id','season','division_id'])
    results_df = results_df.merge(divisions, how='left', 
                                  left_on=['league_id','game_id','season','home_team_division_id'], 
                                  right_on=['league_id','game_id','season','division_id'])
    results_df = results_df.rename(columns={'division_name_x':'away_team_division_name',
                                            'division_name_y':'home_team_division_name'})\
                           .drop(columns=['division_id_x','division_id_y'])
    results_df = results_df[['league_id','game_id','season','week','away_team_id','away_team_manager_id','away_team_name',
                             'away_team_nickname','away_team_division_id','away_team_division_name','away_team_actual',
                             'away_team_projected','home_team_id','home_team_manager_id','home_team_name','home_team_nickname',
                             'home_team_division_id','home_team_division_name','home_team_actual','home_team_projected']]

    return results_df

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

    # get division assignments
    divisions = get_divisions(private_json_path, game_code, game_ids)
    # get matchup results
    results_df = get_all_season_matchups(private_json_path, game_code, game_ids)
    # merge division assignments with matchup results
    results_df = combine_matchups_divisions(results_df, divisions)
    
    ############################
    ### write output to disk ###
    ############################

    # divisions
    data_path = os.path.join(current_script_dir, 'data/divisions.csv')
    divisions.to_csv(data_path, header=True, index=False)

    # matchup results
    data_path = os.path.join(current_script_dir, 'data/matchup_results.csv')
    results_df.to_csv(data_path, header=True, index=False)

if __name__ == '__main__':
    main()