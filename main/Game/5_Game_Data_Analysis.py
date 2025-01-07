import json
from collections import defaultdict
import matplotlib.pyplot as plt

# Load the game data
with open("../../Data/Game/2_steam_games_with_genres.json", "r", encoding="utf-8") as file:
    games = json.load(file)

with open("../../Data/Game/4_steam_unplayed_games_with_igdb.json", "r", encoding="utf-8") as file:
    unplayed_games = json.load(file)

# Helper function to sort and filter games
def get_top_games(games_list, key, top_n=5):
    return sorted(games_list, key=lambda x: x[key], reverse=True)[:top_n]

# 1. Most Purchased Genres
genre_counts = defaultdict(int)
for game in games:
    for genre in game["genres"]:
        genre_counts[genre] += 1

# Save most purchased genres as JSON
most_purchased_genres = sorted(genre_counts.items(), key=lambda x: x[1], reverse=True)
with open("../../Data/Game/5_most_purchased_genres.json", "w") as file:
    json.dump(most_purchased_genres, file, indent=4)

# Visualization: Bar chart for most purchased genres
plt.figure(figsize=(10, 6))
genres, counts = zip(*most_purchased_genres)
plt.bar(genres, counts, color="skyblue")
plt.xlabel("Genres")
plt.ylabel("Number of Games")
plt.title("Most Purchased Genres")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.savefig('../../Data/Game/most_purchased_genres.png')
plt.show()

# 2. Playtime by Genre
genre_playtime = defaultdict(float)  # Total playtime per genre
playtime_top_games = defaultdict(list)

for game in games:
    for genre in game["genres"]:
        genre_playtime[genre] += game.get("playtime_hours", 0)
        playtime_top_games[genre].append({"name": game["name"], "playtime": game.get("playtime_hours", 0)})

playtime_summary = {
    genre: {
        "total_playtime": playtime,
        "top_games": get_top_games(playtime_top_games[genre], "playtime", 3),
    }
    for genre, playtime in genre_playtime.items()
}

# Save playtime summary and genre playtime as JSON
with open("../../Data/Game/6_playtime_top_games.json", "w") as file:
    json.dump(playtime_summary, file, indent=4)

with open("../../Data/Game/7_genre_playtime.json", "w") as file:
    json.dump(genre_playtime, file, indent=4)

# Visualization: Pie chart for total playtime by genre
threshold = 0.05 * sum(genre_playtime.values())
filtered_playtime = {genre: value for genre, value in genre_playtime.items() if value >= threshold}
filtered_playtime["Other"] = sum(value for genre, value in genre_playtime.items() if value < threshold)

plt.figure(figsize=(8, 8))
genres, playtimes = zip(*sorted(filtered_playtime.items(), key=lambda x: x[1], reverse=True))
plt.pie(playtimes, labels=genres, autopct='%1.1f%%', startangle=140)
plt.title("Total Playtime by Genre")
plt.savefig('../../Data/Game/playtime_by_genre.png')
plt.show()

# 3. Achievements by Genre
genre_achievements = defaultdict(int)  # Total achievements per genre
achievement_top_games = defaultdict(list)

for game in games:
    for genre in game["genres"]:
        genre_achievements[genre] += game.get("achievements", 0)
        achievement_top_games[genre].append({
            "name": game["name"],
            "achievements": game.get("achievements", 0),
            "playtime": game.get("playtime_hours", 0)
        })

achievement_summary = {
    genre: {
        "total_achievements": achievements,
        "top_game": get_top_games(achievement_top_games[genre], "achievements", 1)[0],
    }
    for genre, achievements in genre_achievements.items()
}

# Save achievements summary and genre achievements as JSON
with open("../../Data/Game/8_achievements_top_game.json", "w") as file:
    json.dump(achievement_summary, file, indent=4)

with open("../../Data/Game/9_genre_achievements.json", "w") as file:
    json.dump(genre_achievements, file, indent=4)

# Visualization: Horizontal bar chart for achievements by genre
plt.figure(figsize=(10, 6))
genres, total_achievements = zip(
    *sorted([(genre, data["total_achievements"]) for genre, data in achievement_summary.items()], key=lambda x: x[1], reverse=True)
)
plt.barh(genres, total_achievements, color="lightgreen")
plt.xlabel("Total Achievements")
plt.ylabel("Genres")
plt.title("Achievements by Genre")
plt.tight_layout()
plt.savefig('../../Data/Game/achievements_by_genre.png')
plt.show()

# 4. Unplayed Games by Genre
genre_unplayed_games = defaultdict(list)
for game in unplayed_games:
    for genre in game["genres"]:
        genre_unplayed_games[genre].append({"name": game["name"], "rating": game["rating"]})

unplayed_summary = {
    genre: get_top_games(games_list, "rating", 5) for genre, games_list in genre_unplayed_games.items()
}

# Save unplayed games summary as JSON
with open('../../Data/Game/10_unplayed_top_games.json', "w") as file:
    json.dump(unplayed_summary, file, indent=4)
