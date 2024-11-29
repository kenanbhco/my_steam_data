# Steam Profile Analysis Project

## Table of Contents
- [Overview](#overview)
- [Motivation](#motivation)
- [Key Questions](#key-questions)
- [Dataset](#dataset)
  - [Key Attributes](#key-attributes)
- [Project Plan](#project-plan)
  - [1. Data Collection](#1-data-collection)
  - [2. Data Cleaning and Preprocessing](#2-data-cleaning-and-preprocessing)
  - [3. Exploratory Data Analysis (EDA)](#3-exploratory-data-analysis-eda)
  - [4. Findings and Insights](#4-findings-and-insights)
  - [5. Reporting](#5-reporting)
- [Future Work](#future-work)

## Overview
This project analyzes my Steam gaming profile to gain insights into my gaming habits and inform future decisions regarding game purchases and play. By leveraging data from my Steam account, I aim to answer key questions about the games I own, their types, my playtime, achievements, and purchasing trends.

## Motivation
As a gamer with a growing library, I often find it challenging to manage my purchases and discover games I might enjoy playing. This project will help me:
- Identify trends in my gaming preferences.
- Uncover games I own but have not yet played.
- Plan future purchases based on my gaming habits and achievements.
- Organize my budget effectively by understanding the dates when I am most likely to purchase games, such as during sales or seasonal events.
- Optimize my gaming experience by identifying games I might enjoy but have overlooked.

## Key Questions
This project aims to answer the following questions:
1. **Which type of games have I purchased the most?**
2. **Which type of games have I played the most?**
3. **How many games have I bought but never played?**
4. **During which dates did I purchase the most games?**
5. **Which type of games have I collected the most achievements in?**

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

## Project Plan

### 1. Data Collection
- **Steam API**: Retrieve data about games, playtime, and achievements.
- **Steam Website Parsing**: Scrape payment history, including purchase dates and costs, from the Steam website.

### 2. Data Cleaning and Preprocessing
- Organize and clean the data to handle missing or duplicate entries.
- Categorize games by genre.

### 3. Exploratory Data Analysis (EDA)
- Analyze the dataset to answer the outlined questions.
- Generate visualizations to illustrate trends (e.g., bar charts for game genres, heatmaps for purchase dates).

### 4. Findings and Insights
- Summarize insights about my gaming preferences and behavior.
- Provide actionable recommendations for future purchases and gameplay.

### 5. Reporting
- Create a detailed report and update the GitHub repository with:
  - Code for data collection, cleaning, and analysis.
  - Visualizations and findings.
  - Project documentation, including this README.

## Future Work
- **Future Work**: Extend the project by building a recommendation system for identifying games I might enjoy based on my gaming preferences.
