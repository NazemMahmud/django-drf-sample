from django.contrib import admin
from django.urls import path
from applications.tweets.views import *

urlpatterns = [
    path('', home_view),
    path('create-tweet', tweet_create_view),
    path('tweets', tweets_list_view),
]
