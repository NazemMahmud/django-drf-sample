# import random
from django.conf import settings
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view

from .models import Tweet
from .serializers import TweetSerializer

# ALLOWED_HOSTS = settings.ALLOWED_HOSTS
BASE_API_URL = settings.BASE_API_URL


def home_view(request, *args, **kwargs):
    return render(request, "pages/feed.html", {"base_api_url": BASE_API_URL})


@api_view(['POST'])  # now no need of request.POST or (None)
def tweet_create_view(request, *args, **kwargs):
    serializer = TweetSerializer(data=request.POST)
    if serializer.is_valid(raise_exception=True):  # if there is an exception or error, it will automatically send back
        serializer.save(user=request.user)
        return Response(serializer.data, status=201)


@api_view(['GET'])
def tweets_list_view(request, *args, **kwargs):
    query = Tweet.objects.all()  # .order_by('-id');; Now in model, there is meta for ordering
    serializer = TweetSerializer(query, many=True)
    return Response(serializer.data, status=200)


@api_view(['GET'])
def tweets_detail_view(request, tweet_id, *args, **kwargs):
    query = Tweet.objects.filter(id=tweet_id)
    if not query.exists():
        return Response({}, status=404)

    serializer = TweetSerializer(query)
    return Response(serializer.data, status=200)
