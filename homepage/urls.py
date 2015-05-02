from django.conf.urls import patterns, url
from homepage import views

urlpatterns = patterns('',
		url(r'^$', views.index, name='index'),
		url(r'^search_keyword/$', views.search_keyword, name='search_keyword'),
		url(r'^get_tweet_frequency/$', views.get_tweet_frequency, name='get_tweet_frequency'),
		url(r'^get_country_stats/$', views.get_country_stats, name='get_country_stats'),
		url(r'^get_provincial_stats/$', views.get_provincial_stats, name='get_provincial_stats'),
		url(r'^get_regions/$', views.get_regions, name='get_regions'),
		url(r'^daily_province_stats/$', views.daily_province_stats, name='daily_province_stats'),
		url(r'^daily_region_stats/$', views.daily_region_stats, name='daily_region_stats'),
		url(r'^country-stats/(?P<keyword>[\w]+)/$', views.country_stats, name='country_stats'),
		url(r'^region-stats/(?P<region>[\w\d].+)/(?P<keyword>[\w]+)/$', views.region_stats, name='region_stats'),
		url(r'^province-stats/(?P<province>[\w\d].+)/(?P<keyword>[\w\d]+)/$', views.province_stats, name='province_stats'),
	)