# Steam Profile Analysis Project

## Table of Contents
- [Overview](#overview)
- [Motivation](#motivation)
- [Key Questions and Hypotheses](#key-questions-and-hypotheses)
- [Dataset](#dataset)
  - [Key Attributes](#key-attributes)
- [Project Plan](#project-plan)
  - [1. Data Collection](#1-data-collection)
  - [2. Data Cleaning and Preprocessing](#2-data-cleaning-and-preprocessing)
  - [3. Exploratory Data Analysis (EDA)](#3-exploratory-data-analysis-eda)
  - [4. Findings and Insights](#4-findings-and-insights)
  - [5. Reporting](#5-reporting)
- [Future Work](#future-work)

---

## Overview
This project analyzes my Steam gaming profile to address specific questions about unplayed games and purchase trends. The goal is to determine whether there are unplayed games in my library that I might enjoy and to identify trends in my game purchases during Steam sale periods. By leveraging data from my Steam account, I aim to draw actionable insights that could optimize my gaming experience and purchasing behavior.

You can find my presentation here: https://drive.google.com/file/d/1c0nrqGDUcCGOjDnhlddMEJqXRifxY1VW/view?usp=sharing

---

## Motivation
With a growing library of games, it's often challenging to identify titles worth exploring and manage purchasing habits effectively. This project will help me:
- Identify potential hidden gems in my unplayed games library.
- Understand how Steam sale events influence my purchasing behavior.
- Use the findings to inform future gaming decisions, such as prioritizing unplayed games or planning purchases during sales.

---

## Key Questions and Hypotheses

### **Questions**
1. **Are there unplayed games in my library that I might enjoy playing?**
2. **Is there a correlation between Steam sale events and the number of games purchased?**

### **Hypotheses**
1. **Unplayed Games Hypothesis**:  
   *There are unplayed games in my library that align with my gaming preferences and have high ratings, making them worth playing.*  
   This hypothesis will be tested by combining genre-based preferences with game ratings to rank unplayed games.

2. **Steam Sale Hypothesis**:  
   *The number of games purchased significantly increases during Steam sale periods, suggesting a strong correlation between sale events and purchasing behavior.*  
   This hypothesis will be tested by comparing purchase trends during known Steam sale periods with non-sale periods.

---

## Dataset
The data will be sourced from my Steam profile using:
1. **Steam API**: To collect details about owned games, playtime, and achievements.
2. **Steam Website**: Payment history will be obtained by parsing data from the Steam website.

### Key Attributes
- **Game Name**: The title of each game in my library.
- **Game Type**: The genre or category of each game (e.g., RPG, FPS, Puzzle).
- **Playtime**: Total hours played per game.
- **Achievements**: Total achievements unlocked per game.
- **Purchase Date**: The date when the game was purchased.
- **Purchase Cost**: The cost of each game (from payment history).

---

## Project Plan

### 1. Data Collection
- **Steam API**: Retrieve data about games, playtime, and achievements.
- **Steam Website Parsing**: Scrape payment history, including purchase dates and costs, from the Steam website.

### 2. Data Cleaning and Preprocessing
- Organize and clean the data to handle missing or duplicate entries.
- Categorize games by genre and align genres with ratings from external sources (e.g., IGDB).

### 3. Exploratory Data Analysis (EDA)
- Analyze the dataset to answer the outlined questions:
  - Use game ratings and genre preferences to rank unplayed games.
  - Compare the number of games purchased during Steam sale periods with non-sale periods.
- Generate visualizations to illustrate findings (e.g., bar charts, heatmaps).

### 4. Findings and Insights
- Summarize insights about:
  - Unplayed games most likely to align with preferences.
  - Seasonal patterns and the influence of Steam sale events on game purchases.
- Provide actionable recommendations for future gaming decisions.

### 5. Reporting
- Create a detailed report that includes:
  - Code for data collection, cleaning, and analysis.
  - Visualizations and findings.
  - Project documentation, including this README.

---

## Future Work
- Extend the project by developing a recommendation system for unplayed games.
- Explore trends in spending patterns and discounts during sales.
- Incorporate additional data sources, such as user reviews, to refine game rankings.

---
