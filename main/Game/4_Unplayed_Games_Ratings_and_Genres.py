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

def fetch_game_data(access_token, game_name):
    """
    Fetch the genre and rating of a game from IGDB using the game name.
    """
    headers = {
        "Client-ID": CLIENT_ID,
        "Authorization": f"Bearer {access_token}",
    }
    query = f"""
    fields name, genres.name, aggregated_rating;
    search "{game_name}";
    limit 1;
    """

    response = requests.post(IGDB_URL, headers=headers, data=query)
    if response.status_code == 200:
        data = response.json()
        if data:
            genres = [genre["name"] for genre in data[0].get("genres", [])]
            rating = data[0].get("aggregated_rating", "N/A")
            return {"genres": genres, "rating": rating}
    else:
        print(f"Error fetching data for {game_name}: {response.status_code}")
    return {"genres": ["Unknown"], "rating": "N/A"}

def main(client_id, client_secret):
    """
    Main function to fetch game data for unplayed games.
    """
    # Authenticate and get access token
    access_token = get_igdb_access_token(client_id, client_secret)
    if not access_token:
        return

    # Load unplayed games from the Steam API step
    with open("../../Data/Game/3_steam_games_with_zero_playtime.json", "r") as file:
        unplayed_games = json.load(file)

    # Fetch genres and ratings for each unplayed game
    for game in unplayed_games:
        igdb_data = fetch_game_data(access_token, game["name"])
        game["genres"] = igdb_data["genres"]
        game["rating"] = igdb_data["rating"]
        time.sleep(0.5)  # Avoid hitting rate limits

    # Save updated game data
    with open("../../Data/Game/4_steam_unplayed_games_with_igdb.json", "w") as file:
        json.dump(unplayed_games, file, indent=4)

    print(f"Fetched data for {len(unplayed_games)} unplayed games. Data saved to '4_steam_unplayed_games_with_igdb.json'.")

if __name__ == "__main__":
    main(CLIENT_ID, CLIENT_SECRET)
