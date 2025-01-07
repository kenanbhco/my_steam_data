import requests
import json
import time

# Replace with your Twitch Client ID and Secret
CLIENT_ID = "YOUR_ID"
CLIENT_SECRET = "YOUR_SECRET"

# IGDB API URLs
AUTH_URL = "https://id.twitch.tv/oauth2/token"
IGDB_URL = "https://api.igdb.com/v4/games"

def get_igdb_access_token(client_id, client_secret):
    """
    Authenticate with Twitch to get an IGDB access token.
    """
    params = {
        "client_id": client_id,
        "client_secret": client_secret,
        "grant_type": "client_credentials",
    }

    response = requests.post(AUTH_URL, params=params)
    if response.status_code == 200:
        data = response.json()
        return data["access_token"]
    else:
        print(f"Error getting access token: {response.status_code}")
        return None

def fetch_game_genre(access_token, game_name):
    """
    Fetch the genre of a game from IGDB using the game name.
    """
    headers = {
        "Client-ID": CLIENT_ID,
        "Authorization": f"Bearer {access_token}",
    }
    query = f"""
    fields name, genres.name;
    search "{game_name}";
    limit 1;
    """

    response = requests.post(IGDB_URL, headers=headers, data=query)
    if response.status_code == 200:
        data = response.json()
        if data and "genres" in data[0]:
            return [genre["name"] for genre in data[0]["genres"]]
    else:
        print(f"Error fetching genre for {game_name}: {response.status_code}")
    return ["Unknown"]

def main(client_id, client_secret):
    """
    Main function to fetch game genres for the games retrieved from Steam.
    """
    # Authenticate and get access token
    access_token = get_igdb_access_token(client_id, client_secret)
    if not access_token:
        return

    # Load games from the previous step
    with open("../../Data/Game/1_steam_games_with_achievements.json", "r") as file:
        games = json.load(file)

    # Fetch genres for each game
    for game in games:
        game["genres"] = fetch_game_genre(access_token, game["name"])
        # Avoid hitting rate limits
        time.sleep(0.5)

    # Save updated game data
    with open("../../Data/Game/2_steam_games_with_genres.json", "w") as file:
        json.dump(games, file, indent=4)

    print(f"Fetched genres for {len(games)} games. Data saved to '2_steam_games_with_genres.json'.")

if __name__ == "__main__":
    main(CLIENT_ID, CLIENT_SECRET)
