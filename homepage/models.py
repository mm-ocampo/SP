from django.db import models
from django.template.defaultfilters import slugify

# Create your models here.
class Keyword(models.Model):
	word = models.CharField(max_length=128, primary_key=True)
	date = models.DateTimeField()
	searchFrequency = models.PositiveSmallIntegerField(default=1)

	def __str__(self):
		return self.word

class Tweet(models.Model):
	tweetId = models.CharField(max_length=50)
	keyword = models.ForeignKey(Keyword)
	lon = models.FloatField()
	lat = models.FloatField()
	date = models.DateTimeField()
	city = models.CharField(max_length=50, default='')

	def __str__(self):
		return self.tweetId

class Tweetlog(models.Model):
	keyword = models.ForeignKey(Keyword)
	sinceId = models.CharField(max_length=50)
	maxId = models.CharField(max_length=50)
	date = models.DateTimeField()

	def __str__(self):
		return self.keyword.word