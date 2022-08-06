from django.db import models


class Post(models.Model):
	body  = models.TextField()
	title = models.CharField(max_length=200)
	name  = models.CharField(max_length=50)
	price = models.PositiveIntegerField(default=0)

	def __str__(self):
		return self.name