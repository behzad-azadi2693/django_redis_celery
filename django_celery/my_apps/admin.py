from django.contrib import admin

# Register your models here.
from .models import News, Movie

admin.site.register(News)
admin.site.register(Movie)