from django.shortcuts import render

# Create your views here.
from django.db.models import Count, Avg, Q
from django.views.generic import ListView, DetailView
from django.views.generic.base import TemplateView
from .models import NetflixTitle, Country, Director, Category
import json
from django.core.serializers.json import DjangoJSONEncoder

class HomeView(TemplateView):
    """Home page with summary statistics."""
    template_name = 'netflix_app/home.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Summary statistics
        context['total_titles'] = NetflixTitle.objects.count()
        context['total_movies'] = NetflixTitle.objects.filter(type='Movie').count()
        context['total_shows'] = NetflixTitle.objects.filter(type='TV Show').count()
        context['total_countries'] = Country.objects.count()
        context['total_directors'] = Director.objects.count()
        context['total_categories'] = Category.objects.count()
        
        # Latest additions
        context['latest_titles'] = NetflixTitle.objects.order_by('-date_added')[:5]
        
        # Content type distribution for pie chart
        type_counts = list(NetflixTitle.objects.values('type').annotate(count=Count('id')))
        context['type_distribution_json'] = json.dumps([
            {'name': item['type'], 'value': item['count']} for item in type_counts
        ])
        
        # Releases by year for bar chart (last 20 years)
        year_counts = list(NetflixTitle.objects.values('release_year')
                          .filter(release_year__gte=2000)
                          .annotate(count=Count('id'))
                          .order_by('release_year'))
        context['releases_by_year_json'] = json.dumps({
            'years': [item['release_year'] for item in year_counts],
            'counts': [item['count'] for item in year_counts]
        })
        
        return context

class TitleListView(ListView):
    """List view for all Netflix titles with search and filtering."""
    model = NetflixTitle
    template_name = 'netflix_app/title_list.html'
    context_object_name = 'titles'
    paginate_by = 20
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Search functionality
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(
                Q(title__icontains=query) |
                Q(description__icontains=query) |
                Q(cast__icontains=query)
            )
        
        # Filtering
        content_type = self.request.GET.get('type')
        if content_type:
            queryset = queryset.filter(type=content_type)
            
        category_id = self.request.GET.get('category')
        if category_id:
            queryset = queryset.filter(categories__id=category_id)
            
        country_id = self.request.GET.get('country')
        if country_id:
            queryset = queryset.filter(countries__id=country_id)
            
        year = self.request.GET.get('year')
        if year:
            queryset = queryset.filter(release_year=year)
            
        # Sorting
        sort = self.request.GET.get('sort', '-date_added')
        queryset = queryset.order_by(sort)
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add filter options
        context['categories'] = Category.objects.all().order_by('name')
        context['countries'] = Country.objects.annotate(
            title_count=Count('netflixtitle')
        ).order_by('-title_count')[:20]  # Top 20 countries
        
        # Current filter selections
        context['selected_type'] = self.request.GET.get('type', '')
        context['selected_category'] = self.request.GET.get('category', '')
        context['selected_country'] = self.request.GET.get('country', '')
        context['selected_year'] = self.request.GET.get('year', '')
        context['search_query'] = self.request.GET.get('q', '')
        context['sort'] = self.request.GET.get('sort', '-date_added')
        
        return context

class TitleDetailView(DetailView):
    """Detail view for a specific Netflix title."""
    model = NetflixTitle
    template_name = 'netflix_app/title_detail.html'
    context_object_name = 'title'
    slug_field = 'show_id'
    slug_url_kwarg = 'show_id'

class CountryAnalysisView(TemplateView):
    """View for country analysis."""
    template_name = 'netflix_app/country_analysis.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Countries with most content
        top_countries = Country.objects.annotate(
            title_count=Count('netflixtitle')
        ).order_by('-title_count')[:15]
        
        context['top_countries'] = top_countries
        
        # Data for chart
        context['countries_data_json'] = json.dumps([{
            'name': country.name, 
            'count': country.title_count
        } for country in top_countries])
        
        return context

class DirectorAnalysisView(TemplateView):
    """View for director analysis."""
    template_name = 'netflix_app/director_analysis.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Top directors
        top_directors = Director.objects.annotate(
            title_count=Count('netflixtitle')
        ).order_by('-title_count')[:15]
        
        context['top_directors'] = top_directors
        
        # Data for chart
        context['directors_data_json'] = json.dumps([{
            'name': director.name, 
            'count': director.title_count
        } for director in top_directors])
        
        return context

class YearAnalysisView(TemplateView):
    """View for year-based analysis."""
    template_name = 'netflix_app/year_analysis.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Distribution by year
        year_counts = list(NetflixTitle.objects.values('release_year')
                         .annotate(count=Count('id'))
                         .order_by('release_year'))
        
        # Split by type
        movie_year_counts = list(NetflixTitle.objects
                               .filter(type='Movie')
                               .values('release_year')
                               .annotate(count=Count('id'))
                               .order_by('release_year'))
        
        show_year_counts = list(NetflixTitle.objects
                              .filter(type='TV Show')
                              .values('release_year')
                              .annotate(count=Count('id'))
                              .order_by('release_year'))
        
        # Prepare data for chart
        years = sorted(set([item['release_year'] for item in year_counts]))
        
        # Create a dictionary for faster lookups
        movie_counts_dict = {item['release_year']: item['count'] for item in movie_year_counts}
        show_counts_dict = {item['release_year']: item['count'] for item in show_year_counts}
        
        # Prepare final dataset
        movie_data = [movie_counts_dict.get(year, 0) for year in years]
        show_data = [show_counts_dict.get(year, 0) for year in years]
        
        context['years_data_json'] = json.dumps({
            'years': years,
            'movies': movie_data,
            'shows': show_data
        })
        
        return context

class CategoryAnalysisView(TemplateView):
    template_name = 'netflix_app/category_analysis.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        top_categories = Category.objects.annotate(
            title_count=Count('netflixtitle')
        ).order_by('-title_count')[:15]

        context['categories'] = top_categories


        # Ensure proper JSON encoding
        context['categories_data_json'] = json.dumps([
            {'name': category.name, 'count': category.title_count}
            for category in top_categories
        ], cls=DjangoJSONEncoder)

        return context

class SearchView(ListView):
    """Advanced search view."""
    model = NetflixTitle
    template_name = 'netflix_app/search.html'
    context_object_name = 'results'
    paginate_by = 20
    
    def get_queryset(self):
        queryset = NetflixTitle.objects.all()
        
        # Apply filters from the search form
        if self.request.GET:
            # Basic search
            query = self.request.GET.get('q')
            if query:
                queryset = queryset.filter(
                    Q(title__icontains=query) |
                    Q(description__icontains=query) |
                    Q(cast__icontains=query)
                )
            
            # Type filter
            content_type = self.request.GET.get('type')
            if content_type:
                queryset = queryset.filter(type=content_type)
            
            # Category filter
            category = self.request.GET.get('category')
            if category:
                queryset = queryset.filter(categories__id=category)
            
            # Year range
            min_year = self.request.GET.get('min_year')
            if min_year:
                queryset = queryset.filter(release_year__gte=min_year)
                
            max_year = self.request.GET.get('max_year')
            if max_year:
                queryset = queryset.filter(release_year__lte=max_year)
            
            # Rating
            rating = self.request.GET.get('rating')
            if rating:
                queryset = queryset.filter(rating=rating)
            
            # Country
            country = self.request.GET.get('country')
            if country:
                queryset = queryset.filter(countries__id=country)
            
            # Director
            director = self.request.GET.get('director')
            if director:
                queryset = queryset.filter(director__id=director)
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add search form options
        context['categories'] = Category.objects.all().order_by('name')
        context['countries'] = Country.objects.all().order_by('name')
        context['directors'] = Director.objects.all().order_by('name')
        context['ratings'] = NetflixTitle.objects.values_list('rating', flat=True).distinct().order_by('rating')
        
        # Remember current selections
        context['form_data'] = self.request.GET
        
        return context