import json

# Load data
with open("../../Data/Game/4_steam_unplayed_games_with_igdb.json", "r", encoding="utf-8") as file:
    unplayed_games = json.load(file)

with open("../../Data/Game/7_genre_playtime.json", "r", encoding="utf-8") as file:
    genre_playtime = json.load(file)

with open("../../Data/Game/9_genre_achievements.json", "r", encoding="utf-8") as file:
    genre_achievements = json.load(file)

# Step 1: Calculate Genre Points
def calculate_genre_points(playtime, achievements):
    """
    Calculate genre points using proportions of playtime and achievements.
    Uses 70% playtime proportion and 30% achievement proportion.
    """
    total_playtime = sum(playtime.values())
    total_achievements = sum(achievements.values())

    genre_points = {}
    for genre in playtime:
        playtime_proportion = playtime.get(genre, 0) / total_playtime if total_playtime > 0 else 0
        achievement_proportion = achievements.get(genre, 0) / total_achievements if total_achievements > 0 else 0
        genre_points[genre] = (0.7 * playtime_proportion) + (0.3 * achievement_proportion)
    return genre_points


genre_points = calculate_genre_points(genre_playtime, genre_achievements)

# Step 2: Score Unplayed Games
def genre_match_score(game_genres, points):
    """
    Calculate the genre match score for a game based on the highest scoring genre.
    """
    if not game_genres:
        return 0
    scores = [points.get(genre, 0) for genre in game_genres]
    return max(scores) if scores else 0

ranked_games = []
for game in unplayed_games:
    game_genres = game.get("genres", [])
    game_rating = game.get("rating", 0)
    match_score = genre_match_score(game_genres, genre_points)
    weighted_score = (0.6 * game_rating) + (0.4 * match_score)
    ranked_games.append({
        "name": game["name"],
        "genres": game_genres,
        "rating": game_rating,
        "match_score": match_score,
        "weighted_score": weighted_score
    })

# Step 3: Normalize Scores
min_score = min(game["weighted_score"] for game in ranked_games)
max_score = max(game["weighted_score"] for game in ranked_games)

for game in ranked_games:
    game["normalized_score"] = 100 * (game["weighted_score"] - min_score) / (max_score - min_score)

# Step 4: Sort and Save Ranked Games
ranked_games = sorted(ranked_games, key=lambda x: x["normalized_score"], reverse=True)

with open("../../Data/Game/11_ranked_unplayed_games.json", "w", encoding="utf-8") as file:
    json.dump(ranked_games, file, indent=4)

print("Ranked unplayed games saved to '11_ranked_unplayed_games.json'.")
