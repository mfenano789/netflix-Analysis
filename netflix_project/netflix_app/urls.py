# netflix_app/urls.py

from django.urls import path
from . import views

app_name = 'netflix_app'

urlpatterns = [
    # Home page with summary statistics
    path('', views.HomeView.as_view(), name='home'),
    
    # Title listings and details
    path('titles/', views.TitleListView.as_view(), name='title_list'),
    path('title/<str:show_id>/', views.TitleDetailView.as_view(), name='title_detail'),
    
    # Analysis views
    path('analysis/countries/', views.CountryAnalysisView.as_view(), name='country_analysis'),
    path('analysis/directors/', views.DirectorAnalysisView.as_view(), name='director_analysis'),
    path('analysis/years/', views.YearAnalysisView.as_view(), name='year_analysis'),
    path('analysis/categories/', views.CategoryAnalysisView.as_view(), name='category_analysis'),
    
    # Search
    path('search/', views.SearchView.as_view(), name='search'),
]