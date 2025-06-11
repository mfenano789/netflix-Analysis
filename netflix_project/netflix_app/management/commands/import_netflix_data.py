# netflix_app/management/commands/import_netflix_data.py

from django.core.management.base import BaseCommand
import pandas as pd
import numpy as np
from django.db import transaction
from netflix_app.models import NetflixTitle, Country, Director, Category
import datetime

class Command(BaseCommand):
    help = 'Import Netflix data from CSV file'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='Path to the Netflix CSV file')

    def parse_date(self, date_str):
        """Parse Netflix date format to Django compatible date."""
        if pd.isna(date_str):
            return None
        try:
            # Netflix dates are in format "Month Day, Year"
            return datetime.datetime.strptime(date_str.strip(), "%B %d, %Y").date()
        except ValueError:
            # Handle potential alternate formats
            try:
                return datetime.datetime.strptime(date_str.strip(), "%B, %Y").date()
            except:
                self.stdout.write(self.style.WARNING(f"Could not parse date: {date_str}"))
                return None

    def handle(self, *args, **kwargs):
        csv_path = kwargs['csv_file']
        self.stdout.write(self.style.SUCCESS(f"Loading Netflix dataset from {csv_path}..."))
        
        try:
            df = pd.read_csv(csv_path)
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error loading CSV file: {e}"))
            return
        
        # Clean data
        self.stdout.write(self.style.SUCCESS("Cleaning data..."))
        # Fill missing values in categorical columns
        categorical_cols = ['director', 'cast', 'country', 'rating', 'listed_in', 'description']
        for col in categorical_cols:
            if col in df.columns and df[col].isnull().sum() > 0:
                df[col] = df[col].fillna('Unknown')
        
        # Drop rows with missing date_added
        initial_count = len(df)
        df = df.dropna(subset=['date_added'])
        self.stdout.write(self.style.SUCCESS(f"Dropped {initial_count - len(df)} rows with missing date_added"))
        
        with transaction.atomic():
            # First create all countries
            self.stdout.write(self.style.SUCCESS("Creating countries..."))
            all_countries = set()
            for countries_str in df['country'].dropna():
                if countries_str != 'Unknown':
                    for country in countries_str.split(', '):
                        all_countries.add(country.strip())
            
            country_objects = {}
            for country_name in all_countries:
                country, created = Country.objects.get_or_create(name=country_name)
                country_objects[country_name] = country
            
            # Then create all directors
            self.stdout.write(self.style.SUCCESS("Creating directors..."))
            all_directors = set()
            for directors_str in df['director'].dropna():
                if directors_str != 'Unknown':
                    for director in directors_str.split(', '):
                        all_directors.add(director.strip())
            
            director_objects = {}
            for director_name in all_directors:
                director, created = Director.objects.get_or_create(name=director_name)
                director_objects[director_name] = director
            
            # Then create all categories
            self.stdout.write(self.style.SUCCESS("Creating categories..."))
            all_categories = set()
            for categories_str in df['listed_in'].dropna():
                for category in categories_str.split(', '):
                    all_categories.add(category.strip())
            
            category_objects = {}
            for category_name in all_categories:
                category, created = Category.objects.get_or_create(name=category_name)
                category_objects[category_name] = category
            
            # Finally create all Netflix titles with their relationships
            self.stdout.write(self.style.SUCCESS("Creating Netflix titles..."))
            created_count = 0
            error_count = 0
            
            for _, row in df.iterrows():
                try:
                    # Parse date
                    date_added = self.parse_date(row['date_added'])
                    if not date_added:
                        continue  # Skip if date cannot be parsed
                    
                    # Check if title already exists
                    if NetflixTitle.objects.filter(show_id=row['show_id']).exists():
                        continue
                    
                    # Create the title
                    title = NetflixTitle(
                        show_id=row['show_id'],
                        type=row['type'],
                        title=row['title'],
                        cast=row['cast'],
                        date_added=date_added,
                        release_year=row['release_year'],
                        rating=row['rating'],
                        duration=row['duration'],
                        description=row['description']
                    )
                    title.save()
                    created_count += 1
                    
                    # Add many-to-many relationships
                    # Add countries
                    if row['country'] and row['country'] != 'Unknown':
                        for country_name in row['country'].split(', '):
                            country_name = country_name.strip()
                            if country_name in country_objects:
                                title.countries.add(country_objects[country_name])
                    
                    # Add directors
                    if row['director'] and row['director'] != 'Unknown':
                        for director_name in row['director'].split(', '):
                            director_name = director_name.strip()
                            if director_name in director_objects:
                                title.director.add(director_objects[director_name])
                    
                    # Add categories
                    if 'listed_in' in row and row['listed_in']:
                        for category_name in row['listed_in'].split(', '):
                            category_name = category_name.strip()
                            if category_name in category_objects:
                                title.categories.add(category_objects[category_name])
                
                except Exception as e:
                    error_count += 1
                    self.stdout.write(self.style.ERROR(f"Error processing row {row['show_id']}: {e}"))
                
                # Print progress every 100 titles
                if created_count % 100 == 0:
                    self.stdout.write(f"Created {created_count} titles so far...")
        
        # Print summary
        self.stdout.write(self.style.SUCCESS(f"Import complete!"))
        self.stdout.write(self.style.SUCCESS(f"Created {Country.objects.count()} countries"))
        self.stdout.write(self.style.SUCCESS(f"Created {Director.objects.count()} directors"))
        self.stdout.write(self.style.SUCCESS(f"Created {Category.objects.count()} categories"))
        self.stdout.write(self.style.SUCCESS(f"Created {created_count} Netflix titles"))
        if error_count > 0:
            self.stdout.write(self.style.WARNING(f"Encountered {error_count} errors during import"))