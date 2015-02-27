from django.shortcuts import render
from django.http import HttpResponse
from django.core import serializers
from datetime import datetime
from homepage.models import Tweet, Keyword, Tweetlog
from ftfy import fix_text
import json
import tweepy
import geocoder

# Create your views here.

consumer_key = "C42Xh9gXP9i2h9kKXgBAjBrBz"
consumer_secret = "gPIDYFqVNT4mN0ZCtei9LQDfe9JvOIushZrpqJFbBDbmTtVPkk"
access_token = "320102909-QkVoZcIR5hPTxhlJd6u2nWEavBwZIYyIOv0kCJKf"
access_token_secret = "TBUV4UlzVIJ7pp2sVlrD4WiaXMvIkzI1v7NTW7BB0ovn1"

def index(request):
	topSearch = Keyword.objects.order_by('-searchFrequency')[:5]
	context_dict = {'topSearch': topSearch}
	return render(request, 'homepage/index.html', context_dict)

def search_keyword(request):
	context_dict = {}
	if request.method == 'GET':
		keyword = fix_text(request.GET['keyword'])
		auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
		auth.set_access_token(access_token, access_token_secret)

		# insert/update keyword to database
		try:
			k = Keyword.objects.get(word=keyword)
			if k:
				k.searchFrequency += 1
				k.date = datetime.now()
				k.save()
		except Keyword.DoesNotExist:
			k = Keyword(word = keyword, date = datetime.now())
			k.save()

		# search tweets
		# log = Keyword.objects.get(word=keyword)
		api = tweepy.API(auth)
		places = api.geo_search(query="Philippines", granularity="country")
		place_id = places[0].id
		tweets = api.search(q=keyword+ " place:%s" % place_id, count=20)
		for tweet in tweets:
			tweetId = tweet.id_str
			lon = tweet.coordinates['coordinates'][0]
			lat = tweet.coordinates['coordinates'][1]
			date = tweet.created_at
			insert_tweet(tweetId, k, lon, lat, date)
		sinceId = tweets[0].id_str
		maxId = tweets[len(tweets) - 1].id_str

		# save/update to tweetlog
		try:
			t = Tweetlog.objects.get(keyword=keyword)
			if t:
				t.sinceId = sinceId
				t.maxId = maxId
				t.date = datetime.now()
				t.save()
		except Tweetlog.DoesNotExist:
			t = Tweetlog(keyword = k, sinceId = sinceId, maxId = maxId, date = datetime.now())
			t.save()

		# get markers
		m = Tweet.objects.filter(keyword=keyword)
		json_data = serializers.serialize('json', m)
		print(json_data)
	# return HttpResponse(context_dict)	
	# return HttpResponse(json.dumps(context_dict), content_type='application/json')
	return HttpResponse(json_data, content_type='application/json')

def insert_tweet(tweetId, k, lon, lat, date):
	g = geocoder.google([lat, lon], method='reverse')
	city = g.city
	t = Tweet(tweetId=tweetId, keyword=k, lon=lon, lat=lat, date=date, city=city)
	t.save()
	return t

