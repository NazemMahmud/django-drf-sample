# import random
from django.conf import settings
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from .models import Tweet
from .serializers import TweetSerializer, TweetActionSerializer, TweetCreateSerializer

# ALLOWED_HOSTS = settings.ALLOWED_HOSTS
BASE_API_URL = settings.BASE_API_URL


def home_view(request, *args, **kwargs):
    return render(request, "pages/feed.html", {"base_api_url": BASE_API_URL})


@api_view(['POST'])  # now no need of request.POST or (None)
@permission_classes([IsAuthenticated])
def tweet_create_view(request, *args, **kwargs):
    serializer = TweetCreateSerializer(data=request.data)
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

    serializer = TweetSerializer(query.first())
    return Response(serializer.data, status=200)


@api_view(['DELETE', 'POST'])
@permission_classes([IsAuthenticated])
def tweet_delete_view(request, tweet_id, *args, **kwargs):
    query = Tweet.objects.filter(id=tweet_id)
    if not query.exists():
        return Response({'message': 'Tweet not found'}, status=404)

    query = query.filter(user=request.user)
    if not query.exists():
        return Response({'message': 'You are not authenticated'}, status=401)

    data = query.first()
    data.delete()
    return Response({'message': 'Tweet is removed'}, status=200)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def tweet_action_view(request, *args, **kwargs):
    """
        requests.id is needed
        requests.actions option will be: like, unlike, retweet
        :param request:
        :param tweet_id:
        :param args:
        :param kwargs:
        :return:
    """

    serializer = TweetActionSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        data = serializer.validated_data
        tweet_id = data.get('id')
        action = data.get('action')
        content = data.get('content')

        query = Tweet.objects.filter(id=tweet_id)
        if not query.exists():
            return Response({'message': 'Tweet not found'}, status=404)

        tweet = query.first()
        if action == "like":
            tweet.likes.add(request.user)
            serializer = TweetSerializer(tweet)
            return Response(serializer.data, status=200)
        elif action == "unlike":
            tweet.likes.remove(request.user)
            serializer = TweetSerializer(tweet)
            return Response(serializer.data, status=200)
        elif action == "retweet":
            new_tweet = Tweet.objects.create(
                user=request.user,
                parent=tweet,
                content=content,
            )
            serializer = TweetSerializer(new_tweet)
            return Response(serializer.data, status=201)

    return Response({'message': 'Tweet is removed'}, status=200)
