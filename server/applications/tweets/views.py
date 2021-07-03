# import random
from django.conf import settings
from django.http import HttpResponse, Http404, JsonResponse
from django.shortcuts import render, redirect
from django.utils.http import is_safe_url

from .models import Tweet
from .forms import TweetForm

# ALLOWED_HOSTS = settings.ALLOWED_HOSTS
BASE_API_URL = settings.BASE_API_URL


# Create your views here.


def home_view(request, *args, **kwargs):
    return render(request, "pages/feed.html", {"base_api_url": BASE_API_URL})


def tweet_create_view(request, *args, **kwargs):
    form = TweetForm(request.POST or None)  # create form instance & populate with data from request
    if form.is_valid():
        data = form.save(commit=False)  # not saving, just returning the object
        data.save()
        form = TweetForm()

    # if a GET (or any other method) we'll create a blank form
    else:
        form = NameForm()

    return render(request, 'name.html', {'form': form})

'''
* REST API View
* Get all tweets
'''
def tweets_list_view(request, *args, **kwargs):
    query = Tweet.objects.all().order_by('-id')
    list = [{"id": x.id, "content": x.content} for x in query]
    data = { "response": list}
    return JsonResponse(data)
    # return render(request, "tweets/list.html")


def tweets_detail_view(request, tweet_id, *args, **kwargs):
    return render(request, "tweets/detail.html", context={"tweet_id": tweet_id})