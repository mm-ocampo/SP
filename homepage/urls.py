from django.conf.urls import patterns, url
from homepage import views

urlpatterns = patterns('',
		url(r'^$', views.index, name='index'),
		url(r'^search_keyword/$', views.search_keyword, name='search_keyword'),
	)