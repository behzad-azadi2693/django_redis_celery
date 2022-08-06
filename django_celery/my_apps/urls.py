from django.urls import path
from .views import HomePageView, movie, movie_post

app_name='my_apps'

urlpatterns = [
	path('', HomePageView.as_view(), name='home'),
	path('movie_list/', movie, name='movie_list'),
	path('movie_post/', movie_post, name='movie_post'),
]