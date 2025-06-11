from django.db import models

# Create your models here.
class Country(models.Model):
    """Model representing a country where Netflix content was produced."""
    name = models.CharField(max_length=100, unique=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Countries"

class Director(models.Model):
    """Model representing a director of Netflix content."""
    name = models.CharField(max_length=100, unique=True)
    
    def __str__(self):
        return self.name

class Category(models.Model):
    """Model representing a category/genre of Netflix content."""
    name = models.CharField(max_length=50, unique=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Categories"

class NetflixTitle(models.Model):
    """Main model representing a Netflix title (movie or TV show)."""
    TYPE_CHOICES = [
        ('Movie', 'Movie'),
        ('TV Show', 'TV Show'),
    ]
    
    # Basic information
    show_id = models.CharField(max_length=20, unique=True)
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    title = models.CharField(max_length=255)
    
    # Details
    director = models.ManyToManyField(Director, blank=True)
    cast = models.TextField(blank=True, null=True)
    countries = models.ManyToManyField(Country, blank=True)
    date_added = models.DateField()
    release_year = models.IntegerField()
    rating = models.CharField(max_length=20, blank=True, null=True)
    duration = models.CharField(max_length=50, blank=True, null=True)
    
    # Content classification
    categories = models.ManyToManyField(Category, blank=True)
    description = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.title} ({self.type})"
    
    class Meta:
        ordering = ['-date_added']