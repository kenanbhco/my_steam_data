## Running the Steam Profile Analysis Project

This project analyzes your Steam gaming profile to uncover hidden gems in your library and understand purchase behavior. Follow these instructions to explore your Steam data:

**Prerequisites:**

*   Python 3.x installed on your system.
*   API Keys:
    *   You will need API keys for both Steam Web API and IGDB API.
        *   Obtain a Steam Web API key from [https://developer.valvesoftware.com/wiki/Steam_Web_API](https://developer.valvesoftware.com/wiki/Steam_Web_API)
        *   Obtain an IGDB API key from [https://api-docs.igdb.com/](https://api-docs.igdb.com/)
*   Familiarity with Python scripting is recommended.

**Instructions:**

1.  **Project Structure:**
    *   The project is organized into two main directories: `Data` and `main`.
    *   The `Data` directory stores the output files generated by the scripts.
    *   The `main` directory contains Python scripts for data collection, analysis, and visualization.
    *   Inside `main`, there are subfolders for `Game` and `Purchase` scripts.

2.  **API Key Replacement:**
    *   Locate the Python scripts within the `main` directory (e.g., `main\Game\1_Steam_API_Integration.py`).
    *   Open each script in a text editor.
    *   Find the sections where Steam Web API key and/or IGDB API key are required. These will be denoted by comments or variable names indicating "API_KEY".
    *   Replace the placeholder values with your actual API keys.

3.  **Running the Analysis:**
    *   Decide which aspect of your Steam profile you want to analyze: **Games** or **Purchases**.

    *   **Games Analysis:**
        *   To analyze your game library, navigate to the `main\Game` directory.
        *   The scripts within this folder need to be run in a specific order:
            1.  `1_Steam_API_Integration.py`: Fetches game data (playtime, achievements) from Steam using your API key.
            2.  `2_Fetch_Genres_Using_IGDB_API.py`: Retrieves game genres using the IGDB API (requires additional API key).
            3.  `3_Unplayed_Games.py`: Identifies unplayed games in your library.
            4.  `4_Unplayed_Games_Ratings_and_Genres.py`: Combines unplayed games with genre and rating data.
            5.  `5_Game_Data_Analysis.py`: Performs additional analysis on your game data (playtime, achievements, genres).
            6.  `6_Rank_Unplayed_Games.py`: Ranks unplayed games based on user preferences.

    *   **Purchase Analysis:**
        *   To analyze your purchase history, navigate to the `main\Purchase` directory.
        *   Run the script `1_parsed_puschases.py` to parse purchase data from your Steam account. (This script may require manual adjustments depending on how you obtain your purchase history).
        *   Run the script `2_sale_purschase_comparison.py` to analyze purchase trends during Steam sales (requires parsed purchase data from step 1).

4.  **Output Files:**
    *   Each script generates output files (identified by names like `steam_games_with_achievements.json`) within the `Data` directory. These files store the processed data for analysis and visualization.

5.  **Further Exploration:**
    *   The provided scripts offer a starting point for analyzing your Steam profile.
    *   You can modify the scripts or create new ones to explore your data further based on your interests.

**Important Notes:**

*   This project retrieves data from your Steam account. Ensure you understand the privacy implications before proceeding.
*   Replace API key placeholders with your own keys obtained from Steam and IGDB.
*   Running certain scripts is optional and may require additional configuration depending on your data source (e.g., purchase history parsing).

By following these steps and customizing the scripts as needed, you can unlock valuable insights from your Steam gaming profile!