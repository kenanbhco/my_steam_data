import requests
import json

# Replace with your Steam API key and Steam ID
STEAM_API_KEY = "YOUR_API"
STEAM_ID = "YOUR_ID"

# URLs for API endpoints
OWNED_GAMES_URL = "http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/"
USER_STATS_URL = "http://api.steampowered.com/ISteamUserStats/GetUserStatsForGame/v0002/"

def fetch_owned_games(api_key, steam_id):
    """
    Fetch owned games from Steam API.
    Excludes free games and games with zero playtime.
    """
    params = {
        "key": api_key,
        "steamid": steam_id,
        "include_appinfo": True,
        "include_played_free_games": False,
        "format": "json",
    }

    response = requests.get(OWNED_GAMES_URL, params=params)
    if response.status_code == 200:
        data = response.json()
        games = data["response"].get("games", [])
        filtered_games = [
            {
                "name": game["name"],
                "playtime_hours": game["playtime_forever"] / 60,
                "app_id": game["appid"],  # For achievements
            }
            for game in games if game["playtime_forever"] > 0
        ]
        return filtered_games
    else:
        print(f"Error fetching owned games: {response.status_code}")
        return []

def fetch_achievements(api_key, steam_id, app_id):
    """
    Fetch unlocked achievements for a specific game using its App ID.
    """
    params = {
        "key": api_key,
        "steamid": steam_id,
        "appid": app_id,
    }

    response = requests.get(USER_STATS_URL, params=params)
    if response.status_code == 200:
        data = response.json()
        achievements = data.get("playerstats", {}).get("achievements", [])
        return len([ach for ach in achievements if ach.get("achieved", 0) == 1])
    else:
        print(f"Error fetching achievements for app_id {app_id}: {response.status_code}")
        return 0

def main(api_key, steam_id):
    """
    Main function to fetch game data with achievements.
    """
    games = fetch_owned_games(api_key, steam_id)
    for game in games:
        game["achievements"] = fetch_achievements(api_key, steam_id, game["app_id"])

    # Save to JSON for later use
    with open("../../Data/Game/1_steam_games_with_achievements.json", "w") as file:
        json.dump(games, file, indent=4)

    print(f"Fetched {len(games)} games with achievements. Data saved to '1_steam_games_with_achievements.json'.")

if __name__ == "__main__":
    main(STEAM_API_KEY, STEAM_ID)
