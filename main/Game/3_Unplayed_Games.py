import requests
import json

# Replace with your Steam API key and Steam ID
STEAM_API_KEY = "YOUR_API"
STEAM_ID = "YOUR_ID"

# URL for Steam API
OWNED_GAMES_URL = "http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/"

def fetch_unplayed_games(api_key, steam_id):
    """
    Fetch owned games with zero playtime from Steam API.
    Excludes free games and skips fetching achievements.
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
        unplayed_games = [
            {
                "name": game["name"],
                "playtime_hours": game["playtime_forever"] / 60,
                "app_id": game["appid"],
            }
            for game in games if game["playtime_forever"] == 0
        ]
        return unplayed_games
    else:
        print(f"Error fetching owned games: {response.status_code}")
        return []

def main(api_key, steam_id):
    """
    Main function to fetch unplayed games.
    """
    unplayed_games = fetch_unplayed_games(api_key, steam_id)

    # Save to JSON for later use
    with open("../../Data/Game/3_steam_games_with_zero_playtime.json", "w") as file:
        json.dump(unplayed_games, file, indent=4)

    print(f"Fetched {len(unplayed_games)} unplayed games. Data saved to '3_steam_games_with_zero_playtime.json'.")

if __name__ == "__main__":
    main(STEAM_API_KEY, STEAM_ID)
