from django.shortcuts import render
from django.http import HttpResponse
from django.core import serializers
from django.db.models import Count, Max
from django.core.serializers.json import DjangoJSONEncoder
from datetime import datetime, date, timedelta
from django.views.decorators.cache import never_cache
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
provinceRegion = {'butuan city' : 'caraga region - region 13', 'general santos city' : 'soccsksargen - region 12', 'cotabato city' : 'soccsksargen - region 12', 'davao city' : 'davao region - region 11', 'cagayan de oro city' : 'northern mindanao - region 10', 'zamboanga city' : 'zamboanga peninsula - region 9', 'isabela city' : 'zamboanga peninsula - region 9', 'tacloban city' : 'eastern visayas - region 8', 'bohol' : 'central visayas - region 7', 'cebu' : 'central visayas - region 7', 'negros oriental' : 'central visayas - region 7', 'siquijor' : 'central visayas - region 7', 'baguio city' : 'car', 'ncr' : 'ncr', 'ilocos norte' : 'ilocos region - region 1', 'ilocos sur' : 'ilocos region - region 1', 'la union' : 'ilocos region - region 1', 'pangasinan' : 'ilocos region - region 1', 'batanes' : 'cagayan valley - region 2', 'cagayan' : 'cagayan valley - region 2', 'isabela' : 'cagayan valley - region 2', 'nueva vizcaya' : 'cagayan valley - region 2', 'quirino' : 'cagayan valley - region 2', 'abra' : 'car', 'apayao' : 'car', 'benguet' : 'car', 'ifugao' : 'car', 'kalinga' :  'car', 'mountain province' : 'car',  'aurora' : 'central luzon - region 3', 'bataan' : 'central luzon - region 3', 'bulacan' : 'central luzon - region 3', 'nueva ecija' : 'central luzon - region 3', 'pampanga' : 'central luzon - region 3', 'tarlac' : 'central luzon - region 3', 'zambales' : 'central luzon - region 3',  'cavite' : 'calabarzon - region 4a', 'laguna' : 'calabarzon - region 4a', 'batangas' : 'calabarzon - region 4a', 'rizal' : 'calabarzon - region 4a', 'quezon' : 'calabarzon - region 4a', 'occidental mindoro' : 'mimaropa - region 4b', 'oriental mindoro' : 'mimaropa - region 4b', 'marinduque' : 'mimaropa - region 4b', 'romblon' : 'mimaropa - region 4b', 'palawan' : 'mimaropa - region 4b', 'albay' : 'bicol region - region 5', 'camarines norte' : 'bicol region - region 5', 'camarines sur' : 'bicol region - region 5', 'catanduanes' : 'bicol region - region 5', 'masbate' : 'bicol region - region 5', 'sorsogon' : 'bicol region - region 5', 'aklan' : 'western visayas - region 6', 'antique' : 'western visayas - region 6', 'negros occidental' : 'western visayas - region 6', 'capiz' : 'western visayas - region 6', 'guimaras' : 'western visayas - region 6', 'iloilo' : 'western visayas - region 6', 'biliran' : 'eastern visayas - region 8', 'eastern samar' : 'eastern visayas - region 8', 'leyte' : 'eastern visayas - region 8', 'northern samar' : 'eastern visayas - region 8', 'samar' : 'eastern visayas - region 8', 'southern leyte' : 'eastern visayas - region 8', 'zamboanga del norte' : 'zamboanga peninsula - region 9', 'zamboanga del sur' : 'zamboanga peninsula - region 9', 'zamboanga sibugay' : 'zamboanga peninsula - region 9', 'camiguin' : 'northern mindanao - region 10', 'misamis oriental' : 'northern mindanao - region 10', 'lanao del norte' : 'northern mindanao - region 10', 'bukidnon' : 'northern mindanao - region 10', 'misamis occidental' : 'northern mindanao - region 10', 'compostela valley' : 'davao region - region 11', 'davao del norte' : 'davao region - region 11', 'davao del sur' : 'davao region - region 11', 'davao oriental' : 'davao region - region 11', 'davao occidental' : 'davao region - region 11', 'south cotabato' : 'soccsksargen - region 12', 'sultan kudarat' : 'soccsksargen - region 12', 'sarangani' : 'soccsksargen - region 12', 'north cotabato' : 'soccsksargen - region 12',  'agusan del norte' : 'caraga region - region 13', 'agusan del sur' : 'caraga region - region 13', 'surigao del norte' : 'caraga region - region 13', 'surigao del sur' : 'caraga region - region 13', 'dinagat islands' : 'caraga region - region 13', 'basilan' : 'armm', 'lanao del sur' : 'armm', 'maguindanao' : 'armm', 'sulu' : 'armm', 'tawi-tawi' : 'armm'}
regions = {'ilocos region - region 1' : 'region1', 'cagayan valley - region 2' : 'region2', 'central luzon - region 3' : 'region3', 'calabarzon - region 4a' : 'region4a', 'mimaropa - region 4b' : 'region4b', 'bicol region - region 5' : 'region5', 'western visayas - region 6' : 'region6', 'central visayas - region 7' : 'region7', 'eastern visayas - region 8' : 'region8', 'zamboanga peninsula - region 9' : 'region9', 'northern mindanao - region 10' : 'region10', 'davao region - region 11' : 'region11', 'soccsksargen - region 12' : 'region12', 'caraga region - region 13' : 'region13', 'car' : 'car', 'armm' : 'armm', 'ncr' : 'ncr'}
predictionData = []

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
	predictionData = []
	return render(request, 'homepage/index.html', context_dict)

def insert_tweet(tweetId, k, lon, lat, date):
	g = geocoder.google([lat, lon], method='reverse')
	if g.county is not None:
		province = g.county
		if province.lower() in provinceRegion :
			region = provinceRegion[province.lower()]
		else:
			region = "ncr"
	else:
		province = "NCR"
		region = "ncr"
	if g.city is not None:
		city = g.city
	else :
		city = "None"
	t = Tweet(tweetId = tweetId, keyword = k, lon = lon, lat = lat, date = datetime.date(date), city = city.lower(), province = province.lower(), region = region.lower())
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
	print("before try")
	try:
		log = Tweetlog.objects.get(keyword = keyword)
		if log:
			print("pased try and it log")
			tweets = api.search(q = keyword+ " -no -not -wala place:%s" % place_id, count = 100, since_id = int(log.sinceId))
			len(tweets)
	except Tweetlog.DoesNotExist:
		tweets = api.search(q = keyword+ " -no -not -wala place:%s" % place_id, count = 100)
	print(len(tweets))
	return tweets

def search_older_tweets(keyword):
	auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_token, access_token_secret)
	api = tweepy.API(auth)
	places = api.geo_search(query = "Philippines", granularity = "country")
	place_id = places[0].id
	print('here')
	maxId = Tweetlog.objects.get(keyword = keyword).maxId
	tweets = api.search(q = keyword+ " -no -not -wala place:%s" % place_id, count = 100, max_id = int(maxId))
	print(len(tweets))
	if len(tweets) == 1:
		return []
	else:
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
		t = Tweetlog(keyword = keyword, sinceId = sinceId, maxId = maxId, date = datetime.now())
		t.save()
	return t

def get_frequency_per_province(m):
	t = m.values('province').order_by('-province__count').annotate(Count('province'))
	frequencyPerProvince = []
	for item in t:
		temp = {}
		temp['province'] = item['province']
		temp['frequency'] = item['province__count']
		if (item['province']).lower() in populationPerProvince:
			temp['population'] = populationPerProvince[(item['province']).lower()]
		else:
			temp['population'] = 0
		frequencyPerProvince.append(temp)
	return frequencyPerProvince

#ajax for searching tweets
def search_keyword(request):
	if request.method == 'GET':
		keyword = fix_text(request.GET['keyword'])

		# insert/update keyword to database
		k = insert_update_keyword(keyword)
	
		# search tweets
		flag = 0
		tweets = search_tweets(keyword)
		while tweets:
			if tweets:
				temp = []
				# save each tweet details to db
				for tweet in tweets:
					if flag != 0 and tweet.id_str == maxId:
						break
					if tweet.coordinates is not None:
						tweetId = tweet.id_str
						lon = tweet.coordinates['coordinates'][0]
						lat = tweet.coordinates['coordinates'][1]
						date = tweet.created_at
						# insert each tweet to db
						insert_tweet(tweetId, k, lon, lat, date)
						temp.append(tweetId) 
				# sinceId = tweets[0].id_str
				if len(temp) != 0:
					if flag == 0:
						sinceId = temp[0]
					maxId = temp[len(temp) - 1]
				# maxId = tweets[len(tweets) - 1].id_str
				# save/update to tweetlog
				save_update_tweetlog(sinceId, maxId, k)
				tweets = search_older_tweets(keyword)
			else:
				break

		# get all tweet of the keyword from db
		end_date = datetime.date(datetime.now())
		start_date = end_date - timedelta(days = 7)
		m = Tweet.objects.filter(keyword = keyword, date__range=(start_date, end_date))
		markers = serializers.serialize('json', m)

	return HttpResponse(markers, content_type = 'application/json')

# ajax for getting prediction data
@never_cache
def get_tweet_frequency(request):
	if request.method == 'GET':
		keyword = fix_text(request.GET['keyword'])
		daysCount = request.GET['count']
		end_date = datetime.date(datetime.now())
		start_date = end_date - timedelta(days = 7)
		m = Tweet.objects.filter(keyword = keyword, date__range=(start_date, end_date))
		
		if m:
			# get frequency of tweets per province
			frequencyPerProvince = get_frequency_per_province(m)
			for item in frequencyPerProvince:
				if (item['province']).lower() in populationPerProvince:
					item = sir_model(item, populationPerProvince[(item['province']).lower()], keyword, daysCount)
					predictionData.append(item)
		# t = Tweet.objects.filter(keyword = keyword).values('province').order_by('-province__count').annotate(Count('province'))
		# frequencyPerProvince = {}
		# for item in t:
		# 	frequencyPerProvince[item['province']] = item['province__count']
		json_data = json.dumps(list(predictionData), cls = DjangoJSONEncoder)
		# json_data = serializers.serialize('json', predictionData)
		# json_data = json.dumps(frequencyPerProvince, cls = DjangoJSONEncoder)
	return HttpResponse(json_data, content_type = "application/json")

def get_sum_of_x(array_counter):
	total = 0
	for item in array_counter:
		total += item['x']
	return total

def get_sum_of_y(array_counter):
	total = 0
	for item in array_counter:
		total += item['y']
	return total

def get_sum_of_square_of_x(array_counter):
	total = 0
	for item in array_counter:
		total += item['x'] * item['x']
	return total

def get_sum_of_xy(array_counter):
	total = 0
	for item in array_counter:
		total += item['x'] * item['y']
	return total	

def compute_alpha(keyword, province):
	alpha = 1
	end_date = datetime.date(datetime.now())
	start_date = end_date - timedelta(days = 7)
	m = Tweet.objects.filter(keyword = keyword, province = province, date__range=(start_date, end_date))
	array_counter = []
	i = 7
	counter = 1
	while i >= 0:
		array_object = {}
		temp = date.today() - timedelta(days = i)
		i -= 1
		array_object['x'] = counter
		array_object['y'] = len(m.filter(date = temp))
		array_counter.append(array_object)
		counter += 1
	N = len(array_counter)
	sum_of_xy = get_sum_of_xy(array_counter)
	sum_of_x = get_sum_of_x(array_counter)
	sum_of_y = get_sum_of_y(array_counter)
	sum_of_square_of_x = get_sum_of_square_of_x(array_counter)
	alpha = ((N * sum_of_xy) - (sum_of_x - sum_of_y)) / ((N * sum_of_square_of_x) - (sum_of_x * sum_of_x))
	return alpha

def get_ds(alpha, s, i):
	return (-1 * alpha * s * i)

def get_di(alpha, s, i, beta):
	return ((alpha * s * i) - (beta * i))

def get_dr(beta, i):
	return (beta * i)

def sir_model(item, population, keyword, daysCount):
	# based from http://wearesocial.net/tag/philippines/
	# internet users in ph as of 2015 = 37602976
	# active twitter users as of 20115 = 40%
	# twitterPopulation = 37602976 * 0.4
	# internet users in ph as of 2010 = 14800000
	# active twitter users as of 2010 = 24.8
	twitterPopulation = 14800000 * 0.148
	phPopulation = 92337852
		
	# transmitivity rate
	alpha = compute_alpha(keyword, item['province'])
	
	# recovery rate
	beta = 1/7

	# m = Tweet.objects.filter(keyword = keyword, province = item['province'], date = date.today())
	end_date = datetime.date(datetime.now())
	start_date = end_date - timedelta(days = 7)
	m = Tweet.objects.filter(keyword = keyword, province = item['province'], date__range=(start_date, end_date))
	# i1 = round((item['frequency'] * population)/(twitterPopulation * (population/phPopulation)))
	# i1 = round((len(m) * population)/(twitterPopulation * (population/phPopulation))) + 1
	# i1 = round((len(m) * population)/(twitterPopulation * (population/phPopulation))) + 1
	# i1 = round((len(m) * population)/((twitterPopulation * population)/phPopulation)) + 1
	provinceRatio = population/phPopulation
	twitterRatio = twitterPopulation * provinceRatio
	freqRatio = len(m)/twitterRatio
	final = freqRatio * population
	i1 = round(final) + 1
	s1 = population - i1
	r1 = 0
	daysCount = int(daysCount)
	# alpha = alpha / i1

	while daysCount > 0:
		i0 = i1 / population
		s0 = s1 / population
		r0 = r1 / population
		alpha = i0 / alpha
		ds = get_ds(alpha, s0, i0)
		di = get_di(alpha, s0, i0, beta)
		dr = get_dr(beta, i0)
		i1 = i1 + (di * population)
		s1 = s1 + (ds * population)
		r1 = r1 + (dr * population)
		daysCount = daysCount - 1

	item['susceptible']  = s1
	item['infected'] = i1
	item['recovered'] = r1
	item['alpha'] = alpha
	item['ratio'] = (alpha * (s1/population))/beta
	item['percentage'] = item['infected']/population
	return item

# get frequency per day for country stats
def frequency_per_day(t):
	# t = t.values('date').order_by('-date__count').annotate(Count('date'))
	array_counter = []
	i = 7
	while i >= 0:
		array_object = {}
		temp = date.today() - timedelta(days = i)
		i -= 1
		array_object['date'] = temp
		array_object['frequency'] = len(t.filter(date = temp))
		array_counter.append(array_object)
	return array_counter

# ajax get country stats
def get_country_stats(request):
	if request.method == 'GET':
		tweetFrequency = []
		keyword = fix_text(request.GET['keyword'])
		end_date = datetime.date(datetime.now())
		start_date = end_date - timedelta(days = 7)
		m = Tweet.objects.filter(keyword = keyword, date__range=(start_date, end_date))
		
		if m:
			tweetFrequency = frequency_per_day(m)
		json_data = json.dumps(list(tweetFrequency), cls = DjangoJSONEncoder)
	return HttpResponse(json_data, content_type = "application/json")

# ajax get provincial stats
def get_provincial_stats(request):
	if request.method == 'GET':
		provinceFrequency = []
		keyword = fix_text(request.GET['keyword'])
		end_date = datetime.date(datetime.now())
		start_date = end_date - timedelta(days = 7)
		m = Tweet.objects.filter(keyword = keyword, date__range=(start_date, end_date))
		if m:
			provinceFrequency = get_frequency_per_province(m)
		json_data = json.dumps(list(provinceFrequency), cls = DjangoJSONEncoder)
	return HttpResponse(json_data, content_type = "application/json")	

# main controller for country stats
def country_stats(request, keyword):
	keyword = fix_text(keyword)
	topSearch = view_most_searched()
	trending = view_trending()
	context_dict = {'keyword' : keyword, 'topSearch': topSearch, 'trending': trending}
	return render(request, 'homepage/country.html', context_dict)

# ajax get all regions that tweet about the keyword
def get_regions(request):
	if request.method == 'GET':
		keyword = fix_text(request.GET['keyword'])
		end_date = datetime.date(datetime.now())
		start_date = end_date - timedelta(days = 7)
		m = Tweet.objects.filter(keyword = keyword, date__range=(start_date, end_date))
		t = m.values('region').order_by('-region__count').annotate(Count('region'))
	json_data = json.dumps(list(t), cls = DjangoJSONEncoder)
	return HttpResponse(json_data, content_type = "application/json")	

# ajax for getting the daily tweet in a region 
def daily_region_stats(request):
	array_counter = []
	if request.method == 'GET':
		keyword = fix_text(request.GET['keyword'])
		region = fix_text(request.GET['region'])
		end_date = datetime.date(datetime.now())
		start_date = end_date - timedelta(days = 7)
		m = Tweet.objects.filter(region = region, keyword = keyword, date__range=(start_date, end_date))
		i = 7
		while i >= 0:
			temp = date.today() - timedelta(days = i)
			i -= 1
			dateFrequency = {}
			dateFrequency['date'] = temp
			dateFrequency['frequency'] = len(m.filter(date = temp))
			array_counter.append(dateFrequency)
		t = Tweet.objects.filter(keyword = keyword, date__range=(start_date, end_date)).values('region').order_by('-region__count').annotate(Count('region'))
		rank = 1
		for item in t:
			if item['region'] == region:
				break
			else:
				rank += 1
		temp2 = {}
		temp2['rank'] = rank
		array_counter.append(temp2)
	json_data = json.dumps(list(array_counter), cls = DjangoJSONEncoder)
	return HttpResponse(json_data, content_type = "application/json")

# main controller for region stats
def region_stats(request, keyword, region):
	topSearch = view_most_searched()
	trending = view_trending()
	context_dict = {'region' : region, 'keyword' : keyword, 'topSearch': topSearch, 'trending': trending}
	return render(request, 'homepage/region.html', context_dict)

# ajax for getting daily tweets per province
def daily_province_stats(request):
	array_counter = []
	if request.method == 'GET':
		keyword = fix_text(request.GET['keyword'])
		province = fix_text(request.GET['province'])
		end_date = datetime.date(datetime.now())
		start_date = end_date - timedelta(days = 7)
		m = Tweet.objects.filter(province = province, keyword = keyword, date__range=(start_date, end_date))
		i = 7
		while i >= 0:
			temp = date.today() - timedelta(days = i)
			i -= 1
			dateFrequency = {}
			dateFrequency['date'] = temp
			dateFrequency['frequency'] = len(m.filter(date = temp))
			array_counter.append(dateFrequency)
		t = Tweet.objects.filter(keyword = keyword, date__range=(start_date, end_date)).values('province').order_by('-province__count').annotate(Count('province'))
		rank = 1
		for item in t:
			if item['province'] == province:
				break
			else:
				rank += 1
		temp2 = {}
		temp2['rank'] = rank
		array_counter.append(temp2)
	json_data = json.dumps(list(array_counter), cls = DjangoJSONEncoder)
	return HttpResponse(json_data, content_type = "application/json")

# main controller for province stats
def province_stats(request, keyword, province):
	topSearch = view_most_searched()
	trending = view_trending()
	context_dict = {'province' : province, 'keyword' : keyword, 'topSearch': topSearch, 'trending': trending}
	return render(request, 'homepage/province.html', context_dict)