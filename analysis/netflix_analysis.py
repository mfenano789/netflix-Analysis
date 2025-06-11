# Comprehensive Netflix Data Analysis Script
# This script loads a Netflix dataset, cleans it, performs exploratory analysis,
# and creates visualizations to answer specific questions about the data.

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

# Set plot style
plt.style.use('seaborn-v0_8-darkgrid')

# 1. Load the dataset
print("Loading Netflix dataset...")
netflix_df = pd.read_csv('./data/netflix_titles.csv')

# Display basic information about the dataset
print("\nDataset Overview:")
print(f"Number of rows: {netflix_df.shape[0]}")
print(f"Number of columns: {netflix_df.shape[1]}")
print("\nColumn names:")
print(netflix_df.columns.tolist())

# 2. Data Cleaning and Exploratory Analysis
print("\n--- Data Cleaning and Exploratory Analysis ---")

# Check for missing values
print("\nMissing values per column:")
missing_values = netflix_df.isnull().sum()
missing_percentage = (missing_values / len(netflix_df)) * 100
missing_info = pd.DataFrame({
    'Missing Values': missing_values,
    'Percentage': missing_percentage.round(2)
})
print(missing_info)

# Fill missing values in categorical columns
categorical_cols = netflix_df.select_dtypes(include=['object']).columns.tolist()
categorical_cols = [col for col in categorical_cols if col != 'date_added']  # Exclude date_added

print("\nFilling missing values in categorical columns...")
for col in categorical_cols:
    if netflix_df[col].isnull().sum() > 0:
        netflix_df[col] = netflix_df[col].fillna('Unknown')

# Drop rows with missing date_added
print(f"Dropping {netflix_df['date_added'].isnull().sum()} rows with missing date_added...")
netflix_df = netflix_df.dropna(subset=['date_added'])

# Count the number of unique values in each column
print("\nNumber of unique values in each column:")
for col in netflix_df.columns:
    print(f"{col}: {netflix_df[col].nunique()} unique values")

# Find the most frequent movie type
print("\nContent type distribution:")
type_counts = netflix_df['type'].value_counts()
print(type_counts)
most_frequent_type = type_counts.idxmax()
print(f"Most frequent type: {most_frequent_type} ({type_counts[most_frequent_type]} titles)")

# Extract year from release_year column
print("\nRelease year statistics:")
print(f"Min year: {netflix_df['release_year'].min()}")
print(f"Max year: {netflix_df['release_year'].max()}")
print(f"Average year: {netflix_df['release_year'].mean():.2f}")

# Find oldest and newest movie/show based on release_year
oldest_title = netflix_df.loc[netflix_df['release_year'].idxmin()]
newest_title = netflix_df.loc[netflix_df['release_year'].idxmax()]

print("\nOldest title:")
print(f"Title: {oldest_title['title']}")
print(f"Type: {oldest_title['type']}")
print(f"Release Year: {oldest_title['release_year']}")

print("\nNewest title:")
print(f"Title: {newest_title['title']}")
print(f"Type: {newest_title['type']}")
print(f"Release Year: {newest_title['release_year']}")

# 3. Visualizations
print("\n--- Creating Visualizations ---")

# Create a figure with multiple subplots
plt.figure(figsize=(20, 17))

# Which country has the highest number of Netflix titles?
print("\nAnalyzing countries with the most titles...")
# Split country column (as some titles have multiple countries)
countries = netflix_df['country'].str.split(', ', expand=False)
countries_expanded = countries.explode().dropna()
countries_expanded = countries_expanded[countries_expanded != 'Unknown']

top_countries = countries_expanded.value_counts().head(15)

plt.subplot(2, 2, 1)
sns.barplot(x=top_countries.values, y=top_countries.index)
plt.title('Top 15 Countries with the Most Netflix Titles', fontsize=14)
plt.xlabel('Number of Titles', fontsize=12)
plt.tight_layout()

# What are the top directors featured on Netflix?
print("\nFinding top directors...")
# Split directors column and expand to get individual directors
directors = netflix_df['director'].str.split(', ', expand=False)
directors_expanded = directors.explode().dropna()
directors_expanded = directors_expanded[directors_expanded != 'Unknown']

top_directors = directors_expanded.value_counts().head(15)

plt.subplot(2, 2, 2)
sns.barplot(x=top_directors.values, y=top_directors.index)
plt.title('Top 15 Directors on Netflix', fontsize=14)
plt.xlabel('Number of Titles', fontsize=12)
plt.tight_layout()

# Plot a histogram showing distribution of Netflix titles by release year
print("\nPlotting distribution of Netflix titles by release year...")
plt.subplot(2, 1, 2)
sns.histplot(data=netflix_df, x='release_year', bins=30, kde=True)
plt.title('Distribution of Netflix Titles by Release Year', fontsize=14)
plt.xlabel('Release Year', fontsize=12)
plt.ylabel('Number of Titles', fontsize=12)
plt.axvline(netflix_df['release_year'].mean(), color='red', linestyle='--', 
            label=f'Mean Year: {netflix_df["release_year"].mean():.1f}')
plt.legend()
plt.tight_layout()

# Save the visualization
plt.savefig('netflix_analysis_results.png', dpi=300, bbox_inches='tight')
print("\nVisualization saved as 'netflix_analysis_results.png'")

# Additional insights
print("\n--- Additional Insights ---")

# Content by decade
netflix_df['decade'] = (netflix_df['release_year'] // 10) * 10
decades_count = netflix_df['decade'].value_counts().sort_index()
print("\nContent by decade:")
print(decades_count)

# Trend of content types over years
print("\nContent type trends by recent years:")
recent_years = netflix_df[netflix_df['release_year'] >= 2010]
type_by_year = recent_years.groupby(['release_year', 'type']).size().unstack()
print(type_by_year)

print("\nAnalysis complete!")

# Show all plots
plt.show()