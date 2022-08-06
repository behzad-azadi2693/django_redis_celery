from django.shortcuts import render, redirect

# Create your views here.
from django.views import generic
from .models import News, Movie
from .forms import MovieForm
from .tasks import movie_task


class HomePageView(generic.ListView):
    template_name = 'home.html'
    context_objects_name = 'news'

    def get_queryset(self):
    	return News.objects.all()


def movie(request):
    movies = Movie.objects.all()
    return render(request, 'movie.html', {'movies':movies})

def movie_post(request):
    if request.method == 'POST':
        form = MovieForm(request.POST , request.FILES)
        if form.is_valid():
            cd = form.cleaned_data
            movie = Movie.objects.create(title=cd['title'],mv_original=cd['movie'])
            movie_task.delay(movie.id)
            return redirect('my_apps:movie_list')

    else:
        form = MovieForm()
    return render(request, 'movie_post.html', {'form':form})