import requests

from datetime import datetime
from bs4 import BeautifulSoup
from celery import shared_task
from .models import News, Movie
import subprocess
import os


@shared_task(name='read_news')
def web_scrap():
	article_list = []
	try:
		print('starting web scrap ...')
		r = requests.get('https://news.ycombinator.com/rss')
		soup = BeautifulSoup(r.connect, features ='xml')
		articles = soup.findall('item')

		for a in articles:
			title = a.find('title').text
			link = a.find('link').text
			pulished_wrong = a.find('pubDate').text
			published = datetime.strptime(pulished_wrong, '%a, %d %b %Y %H:%M:%S %z')

		article = {
		'title':title,
		'link':link,
		'published':published,
		'source':'hackernewa rss'
		}

		article_list.append(article)
		print('finished scraping the article')

		return save_function(article_list)

	except Exception as e:
		print('The scraping job failed. See exception:')
		print(e)


@shared_task(serializer='json')
def save_function(article_list):
	print('starting')
	new_count = 0

	for article in article_list:
		try:
			News.objects.create(
				title = article['title'],
				link = article['link'],
				published = article['published'],
				source = article['source']
			)
			new_count += 1
		
		except Exception as e:
			print('failed at latest_article is none')
			print(e)
			break
	return print('finished') 


@shared_task
def movie_task(movie_id):
	movie = Movie.objects.get(id=movie_id)
	name = '{}_audio.mp3'.format(movie.mv_original.path.split('.')[0])
	audio = os.system(f'ffmpeg -i {movie.mv_original.path} -vn {name}')
	movie.audio  = "movies/"+name.split('/')[-1]
	movie.save()


@shared_task(name = 'cleanning')
def clean_DB():
    news = News.objects.all().delete()
