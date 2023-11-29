from pathlib import Path
from yfpy import YahooFantasySportsQuery

# Read path from environment variable
private_json_path = Path("/mnt/c/Users/ryanc/Documents/Projects/Fantasy_Football")
league_id = "244805"
game_code = "nfl"

# Setup query
yahoo_query = YahooFantasySportsQuery(auth_dir=private_json_path,
                                      league_id=league_id,
                                      game_code=game_code,
                                      browser_callback=False)

# Fetch league data
league = yahoo_query.get_league_info()

# Print some league details
print(league)