from django.contrib import admin
from homepage.models import Tweet, Keyword, Tweetlog

class TweetAdmin(admin.ModelAdmin):
	list_display = ('tweetId', 'keyword', 'lat', 'lon', 'city', 'date')

class KeywordAdmin(admin.ModelAdmin):
	list_display = ('word', 'date', 'searchFrequency')

class TweetlogAdmin(admin.ModelAdmin):
	list_display = ('keyword', 'sinceId', 'maxId', 'date')

admin.site.register(Tweet, TweetAdmin)
admin.site.register(Keyword, KeywordAdmin)
admin.site.register(Tweetlog, TweetlogAdmin)
