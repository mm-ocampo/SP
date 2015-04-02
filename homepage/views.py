from django.shortcuts import render
from django.http import HttpResponse
from django.core import serializers
from django.db.models import Count, Max
from django.core.serializers.json import DjangoJSONEncoder
from datetime import datetime, date, timedelta
from homepage.models import Tweet, Keyword, Tweetlog
from ftfy import fix_text
import json
import tweepy
import geocoder
import requests

# Create your views here.

consumer_key = "C42Xh9gXP9i2h9kKXgBAjBrBz"
consumer_secret = "gPIDYFqVNT4mN0ZCtei9LQDfe9JvOIushZrpqJFbBDbmTtVPkk"
access_token = "320102909-QkVoZcIR5hPTxhlJd6u2nWEavBwZIYyIOv0kCJKf"
access_token_secret = "TBUV4UlzVIJ7pp2sVlrD4WiaXMvIkzI1v7NTW7BB0ovn1"
populationPerProvince = {'butuan city' : 309709, 'general santos city' : 538086, 'cotabato city' : 271786, 'davao city' : 1449296, 'cagayan de oro city' : 602088, 'zamboanga city' : 807129, 'isabela city' : 97857, 'tacloban city' : 221174, 'bohol' : 1255128, 'cebu' : 2619362, 'negros oriental' : 1286666, 'siquijor' : 91066, 'baguio city' : 318676, 'ncr' : 11855975, 'ilocos norte' : 568017, 'ilocos sur' : 658587, 'la union' : 741906, 'pangasinan' : 2779862, 'batanes' : 16604, 'cagayan' : 1124773, 'isabela' : 1489645, 'nueva vizcaya' : 421355, 'quirino' : 176786, 'abra' : 234733, 'apayao' : 112636, 'benguet' : 403944, 'ifugao' : 191078, 'kalinga' :  201613, 'mountain province' : 154187,  'aurora' : 201233, 'bataan' : 687482, 'bulacan' : 2924433, 'nueva ecija' : 1955373, 'pampanga' : 2014019, 'tarlac' : 1273240, 'zambales' : 534443,  'cavite' : 3090691, 'laguna' : 2669847, 'batangas' : 2377395, 'rizal' : 2484840, 'quezon' : 1740638, 'occidental mindoro' : 452971, 'oriental mindoro' : 785602, 'marinduque' : 227828, 'romblon' : 283930, 'palawan' : 771667, 'albay' : 1233432, 'camarines norte' : 542915, 'camarines sur' : 1822371, 'catanduanes' : 246300, 'masbate' : 834650, 'sorsogon' : 740743, 'aklan' : 535725, 'antique' : 546031, 'negros occidental' : 2396039, 'capiz' : 719685, 'guimaras' : 162943, 'iloilo' :  1805576, 'biliran' : 161760, 'eastern samar' : 428877, 'leyte' : 1567984, 'northern samar' : 589013, 'samar' : 733377, 'southern leyte' : 399137, 'zamboanga del norte' : 957997, 'zamboanga del sur' : 959685, 'zamboanga sibugay' : 584685, 'camiguin' : 83807, 'misamis oriental' : 813856, 'lanao del norte' : 607917, 'bukidnon' : 1299192, 'misamis occidental' : 567642, 'compostela valley' : 687195, 'davao del norte' : 945764, 'davao del sur' : 574910, 'davao oriental' : 517618, 'davao occidental' : 293780, 'south cotabato' : 827200, 'sultan kudarat' : 747087, 'sarangani' : 498904, 'north cotabato' : 1226508,  'agusan del norte' : 332487, 'agusan del sur' : 656418, 'surigao del norte' : 442588, 'surigao del sur' : 561219, 'dinagat islands' : 126803, 'basilan' : 293322, 'lanao del sur' : 933260, 'maguindanao' : 944718, 'sulu' : 718290, 'tawi-tawi' : 366550}

def view_most_searched():
	k = Keyword.objects.order_by('-searchFrequency')[:10]
	return k

def view_trending():
	t = Tweet.objects.values('keyword').order_by('-keyword__count').annotate(Count('keyword'))[:10]
	return t

def index(request):
	topSearch = view_most_searched()
	trending = view_trending()
	context_dict = {'topSearch': topSearch, 'trending': trending}
	return render(request, 'homepage/index.html', context_dict)

def insert_tweet(tweetId, k, lon, lat, date):
	g = geocoder.google([lat, lon], method='reverse')
	if g.county is not None:
		province = g.county
	else:
		province = "NCR"
	city = g.city
	t = Tweet(tweetId = tweetId, keyword = k, lon = lon, lat = lat, date = datetime.date(date), city = city, province = province)
	t.save()
	return t

def insert_update_keyword(keyword):
	try:
		k = Keyword.objects.get(word = keyword)
		if k:
			k.searchFrequency += 1
			k.date = datetime.now()
			k.save()
	except Keyword.DoesNotExist:
		k = Keyword(word = keyword, date = datetime.now())
		k.save()
	return k

def search_tweets(keyword):
	auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_token, access_token_secret)
	api = tweepy.API(auth)
	places = api.geo_search(query = "Philippines", granularity = "country")
	place_id = places[0].id
	try:
		log = Tweetlog.objects.get(keyword = keyword)
		if log:
			tweets = api.search(q = keyword+ " place:%s" % place_id, count = 100, since_id = int(log.sinceId))
	except Tweetlog.DoesNotExist:
		tweets = api.search(q = keyword+ " place:%s" % place_id, count = 100)
	return tweets

def save_update_tweetlog(sinceId, maxId, keyword):
	try:
		t = Tweetlog.objects.get(keyword = keyword)
		if t:
			t.sinceId = sinceId
			t.maxId = maxId
			t.date = datetime.now()
			t.save()
	except Tweetlog.DoesNotExist:
		t = Tweetlog(keyword = k, sinceId = sinceId, maxId = maxId, date = datetime.now())
		t.save()

def get_frequency_per_province(m):
	t = m.values('province').order_by('-province__count').annotate(Count('province'))
	frequencyPerProvince = []
	for item in t:
		temp = {}
		temp['province'] = item['province']
		temp['frequency'] = item['province__count']
		frequencyPerProvince.append(temp)
	return frequencyPerProvince

def search_keyword(request):
	if request.method == 'GET':
		keyword = fix_text(request.GET['keyword'])

		# insert/update keyword to database
		k = insert_update_keyword(keyword)

		# search tweets
		tweets = search_tweets(keyword)
			
		if tweets:
			# save each tweet details to db
			for tweet in tweets:
				tweetId = tweet.id_str
				if tweet.coordinates is not None:
					lon = tweet.coordinates['coordinates'][0]
					lat = tweet.coordinates['coordinates'][1]
					date = tweet.created_at
					# insert each tweet to db
					insert_tweet(tweetId, k, lon, lat, date)
			sinceId = tweets[0].id_str
			maxId = tweets[len(tweets) - 1].id_str
			
			# save/update to tweetlog
			save_update_tweetlog(sinceId, maxId)

		# get all tweet of the keyword from db
		m = Tweet.objects.filter(keyword = keyword)
		markers = serializers.serialize('json', m)

		if m:
			# get frequency of tweets per province
			frequencyPerProvince = get_frequency_per_province(m)
			for item in frequencyPerProvince:
				if (item['province']).lower() in populationPerProvince:
					item = sir_model(item, populationPerProvince[(item['province']).lower()])

	return HttpResponse(markers, content_type = 'application/json')


def get_tweet_frequency(request):
	if request.method == 'GET':
		keyword = fix_text(request.GET['keyword'])
		t = Tweet.objects.filter(keyword = keyword).values('province').order_by('-province__count').annotate(Count('province'))
		frequencyPerProvince = {}
		for item in t:
			frequencyPerProvince[item['province']] = item['province__count']
		# json_data = json.dumps(list(t), cls = DjangoJSONEncoder)
		json_data = json.dumps(frequencyPerProvince, cls = DjangoJSONEncoder)
	return HttpResponse(json_data, content_type = "application/json")


# def compute_alpha(keyword, province):
# 	t = Tweet.objects.filter(province = province).values('date').order_by('-date__count').annotate(Count('date'))
# 	alpha = 1
# 	array_counter = []
# 	i = 6
# 	while i >= 0:
# 		temp = date.today() - timedelta(days = i)
# 		i -= 1
# 		dateFrequency = {}
# 		for item in t:
# 			if datetime.date(item['date']) == temp :
# 				dateFrequency[temp] = item['date__count']
# 				break
# 			else :
# 				dateFrequency[temp] = 0
# 		array_counter.append(dateFrequency)
# 	return alpha

def get_ds(alpha, s, i):
	return (-1 * alpha * s * i)

def get_di(alpha, s, i, beta):
	return ((alpha * s * i) - (beta * i))

def get_dr(beta, i):
	return (beta * i)

def sir_model(item, population):
	# transmitivity rate
	alpha = 1/2
	# recovery rate
	beta = 1/7

	i0 = item['frequency']
	s0 = population - i0 
	r0 = 0

	ds = get_ds(alpha, s0, i0)
	di = get_di(alpha, s0, i0, beta)
	dr = get_dr(beta, i0)
	print(ds, di, dr)

	return item