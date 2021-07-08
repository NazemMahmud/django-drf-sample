from django.urls import path
from applications.tweets.views import *

urlpatterns = [
    path('', tweets_list_view),
    path('create', tweet_create_view),
    path('<int:tweet_id>', tweets_detail_view),
    path('action', tweet_action_view),
    path('<int:tweet_id>/delete/', tweet_delete_view),
]
