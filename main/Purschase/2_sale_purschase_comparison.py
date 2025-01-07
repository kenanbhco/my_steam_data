import json
import pandas as pd
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

# Turkish month abbreviations mapping
tr_month_map = {
    'Oca': '01', 'Şub': '02', 'Mar': '03', 'Nis': '04',
    'May': '05', 'Haz': '06', 'Tem': '07', 'Ağu': '08',
    'Eyl': '09', 'Eki': '10', 'Kas': '11', 'Ara': '12'
}

sale_periods = [
    {"name": "Winter Sale", "start": "2023-12-21", "end": "2024-01-04"},
    {"name": "Summer Sale", "start": "2023-06-29", "end": "2023-07-13"},
    {"name": "Winter Sale", "start": "2022-12-22", "end": "2023-01-05"},
    {"name": "Summer Sale", "start": "2022-06-23", "end": "2022-07-07"},
    {"name": "Winter Sale", "start": "2021-12-22", "end": "2022-01-05"},
    {"name": "Summer Sale", "start": "2021-06-24", "end": "2021-07-08"},
    {"name": "Winter Sale", "start": "2020-12-22", "end": "2021-01-05"},
    {"name": "Summer Sale", "start": "2020-06-25", "end": "2020-07-09"},
    {"name": "Winter Sale", "start": "2019-12-19", "end": "2020-01-02"},
    {"name": "Summer Sale", "start": "2019-06-25", "end": "2019-07-09"},
    {"name": "Winter Sale", "start": "2018-12-20", "end": "2019-01-03"},
    {"name": "Summer Sale", "start": "2018-06-21", "end": "2018-07-05"},
    {"name": "Winter Sale", "start": "2017-12-21", "end": "2018-01-04"},
    {"name": "Summer Sale", "start": "2017-06-22", "end": "2017-07-05"},
    {"name": "Winter Sale", "start": "2016-12-22", "end": "2017-01-02"},
    {"name": "Summer Sale", "start": "2016-06-23", "end": "2016-07-04"}
]

def convert_tr_date(date_str):
    """Convert Turkish date string to datetime object"""
    day, month, year = date_str.split()
    month = tr_month_map[month]
    return datetime.strptime(f"{year}-{month}-{day}", "%Y-%m-%d")


def is_within_analysis_period(date, sale_periods):
    """Check if date falls within our analysis period"""
    earliest_sale = min(datetime.strptime(sale['start'], '%Y-%m-%d') for sale in sale_periods)
    latest_sale = max(datetime.strptime(sale['end'], '%Y-%m-%d') for sale in sale_periods)
    return earliest_sale <= date <= latest_sale


def is_during_sale(date, sale_periods):
    """Check if a date falls within any sale period"""
    for sale in sale_periods:
        start = datetime.strptime(sale['start'], '%Y-%m-%d')
        end = datetime.strptime(sale['end'], '%Y-%m-%d')
        if start <= date <= end:
            return True, sale['name']
    return False, None


def analyze_purchase_data(data1, data2, group_name=""):
    """Perform statistical analysis comparing two groups"""
    if len(data1) == 0 or len(data2) == 0:
        return None

    # Mann-Whitney U test
    statistic, p_value = stats.mannwhitneyu(
        data1,
        data2,
        alternative='greater'
    )

    # Effect size (Cohen's d)
    n1, n2 = len(data1), len(data2)
    var1, var2 = np.var(data1, ddof=1), np.var(data2, ddof=1)
    pooled_se = np.sqrt(((n1 - 1) * var1 + (n2 - 1) * var2) / (n1 + n2 - 2))
    effect_size = (np.mean(data1) - np.mean(data2)) / pooled_se

    return {
        'statistic': statistic,
        'p_value': p_value,
        'effect_size': effect_size,
        'count': len(data1),
        'mean': np.mean(data1),
        'median': np.median(data1),
        'std': np.std(data1)
    }


# Load and prepare data
with open('../../Data//Purchase/parsed_purchases.json', 'r', encoding='utf-8') as f:
    purchases = json.load(f)

# Get analysis period boundaries
earliest_sale = min(datetime.strptime(sale['start'], '%Y-%m-%d') for sale in sale_periods)
latest_sale = max(datetime.strptime(sale['end'], '%Y-%m-%d') for sale in sale_periods)

# Convert data to DataFrame with sale period indicators
purchase_data = []
out_of_range_purchases = []

for purchase in purchases:
    date = convert_tr_date(purchase['date'])

    if not is_within_analysis_period(date, sale_periods):
        out_of_range_purchases.append(purchase['date'])
        continue

    during_sale, sale_name = is_during_sale(date, sale_periods)
    sale_season = sale_name.split()[0] if sale_name else "Non-Sale"

    purchase_data.append({
        'date': date,
        'num_games': purchase['number of purchased games in that date'],
        'total_cost': float(purchase['total cost'].replace(' TL', '')),
        'during_sale': during_sale,
        'sale_season': sale_season
    })

df = pd.DataFrame(purchase_data)

# Print date range information
print("\nAnalysis Period Information:")
print(f"Earliest sale in data: {earliest_sale.strftime('%d %b %Y')}")
print(f"Latest sale in data: {latest_sale.strftime('%d %b %Y')}")
print(f"Number of purchases excluded (out of range): {len(out_of_range_purchases)}")
if out_of_range_purchases:
    print("\nOut of range purchase dates:")
    for date in sorted(out_of_range_purchases):
        print(f"Date outside sale periods range: {date}")

# Analyze overall sale effect
sale_games = df[df['during_sale']]['num_games']
non_sale_games = df[~df['during_sale']]['num_games']
overall_stats = analyze_purchase_data(sale_games, non_sale_games, "Overall Sales")

# Analyze individual seasons
sale_seasons = ['Summer', 'Winter']
season_stats = {}

for season in sale_seasons:
    season_data = df[df['sale_season'] == season]['num_games']
    if len(season_data) > 0:
        season_stats[season] = analyze_purchase_data(season_data, non_sale_games, season)

# Visualizations
plt.figure(figsize=(15, 20))

# Add text box with date range information
date_info = f"Analysis Period:\n{earliest_sale.strftime('%d %b %Y')} - {latest_sale.strftime('%d %b %Y')}"

# 1. Overall Sale vs Non-Sale Box Plot
plt.subplot(4, 1, 1)
sns.boxplot(x='during_sale', y='num_games', data=df, palette=['#CCCCCC', '#66B2FF'])
plt.title('Distribution of Games Purchased (Sale vs Non-Sale)', pad=20, fontsize=12)
plt.xlabel('During Sale', fontsize=10)
plt.ylabel('Number of Games', fontsize=10)
plt.text(0.02, 0.98, date_info, transform=plt.gca().transAxes,
         verticalalignment='top', bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))

# 2. Box Plot by Sale Season
plt.subplot(4, 1, 2)
sns.boxplot(x='sale_season', y='num_games', data=df, palette='husl')
plt.title('Distribution of Games Purchased by Sale Season', pad=20, fontsize=12)
plt.xticks(rotation=45)
plt.xlabel('Sale Season', fontsize=10)
plt.ylabel('Number of Games', fontsize=10)

# 3. Violin Plot by Sale Season
plt.subplot(4, 1, 3)
sns.violinplot(x='sale_season', y='num_games', data=df, palette='husl')
plt.title('Distribution Density of Games Purchased by Sale Season', pad=20, fontsize=12)
plt.xticks(rotation=45)
plt.xlabel('Sale Season', fontsize=10)
plt.ylabel('Number of Games', fontsize=10)

# 4. Time Series Plot
plt.subplot(4, 1, 4)
colors = {'Summer': '#FF9999', 'Winter': '#66B2FF', 'Non-Sale': '#CCCCCC'}

for season in df['sale_season'].unique():
    season_data = df[df['sale_season'] == season]
    plt.scatter(season_data['date'], season_data['num_games'],
                label=season, alpha=0.6, color=colors[season], s=50)

plt.title('Games Purchased Over Time by Sale Season', pad=20, fontsize=12)
plt.xlabel('Date', fontsize=10)
plt.ylabel('Number of Games', fontsize=10)
plt.legend(fontsize=10)

plt.tight_layout(pad=3.0)
# Print Results
print("\nSteam Purchase Analysis Results")
print("==============================")

if overall_stats:
    print("\nOverall Sale Effect Analysis:")
    print("-----------------------------")
    print(f"Total purchases analyzed: {len(df)}")
    print(f"Total purchases during sales: {len(sale_games)}")
    print(f"Total purchases outside sales: {len(non_sale_games)}")
    print(f"Mean purchases during sales: {overall_stats['mean']:.2f}")
    print(f"Median purchases during sales: {overall_stats['median']:.2f}")
    print(f"Mean purchases outside sales: {np.mean(non_sale_games):.2f}")
    print(f"Median purchases outside sales: {np.median(non_sale_games):.2f}")
    print(f"Mann-Whitney U statistic: {overall_stats['statistic']:.4f}")
    print(f"P-value: {overall_stats['p_value']:.4f}")
    print(f"Effect size (Cohen's d): {overall_stats['effect_size']:.4f}")

    effect_size = abs(overall_stats['effect_size'])
    if effect_size < 0.2:
        effect_magnitude = "small"
    elif effect_size < 0.5:
        effect_magnitude = "medium"
    else:
        effect_magnitude = "large"

    print(f"Overall effect magnitude: {effect_magnitude}")
    if overall_stats['p_value'] < 0.05:
        print("Sales show a significant overall effect on purchase behavior")
    else:
        print("No significant overall effect detected for sales")

# Print individual season analyses
print("\nAnalysis by Sale Season:")
print("----------------------")
for season in sale_seasons:
    if season in season_stats:
        stats = season_stats[season]
        print(f"\n{season} Sale Analysis:")
        print(f"Total purchases during {season} sales: {stats['count']}")
        print(f"Mean purchases during {season} sales: {stats['mean']:.2f}")
        print(f"Median purchases during {season} sales: {stats['median']:.2f}")
        print(f"Mann-Whitney U statistic: {stats['statistic']:.4f}")
        print(f"P-value: {stats['p_value']:.4f}")
        print(f"Effect size (Cohen's d): {stats['effect_size']:.4f}")

        effect_size = abs(stats['effect_size'])
        if effect_size < 0.2:
            effect_magnitude = "small"
        elif effect_size < 0.5:
            effect_magnitude = "medium"
        else:
            effect_magnitude = "large"

        print(f"Effect magnitude: {effect_magnitude}")
        if stats['p_value'] < 0.05:
            print(f"The {season} sale shows a significant effect on purchase behavior")
        else:
            print(f"No significant effect detected for {season} sale")

save_path = '../../Data/Purchase/steam_purchase_analysis_complete.png'
plt.savefig(save_path)
print("\nVisualization saved as 'steam_purchase_analysis_complete.png'")