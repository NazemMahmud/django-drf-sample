# import random
from django.conf import settings
from django.http import HttpResponse, Http404, JsonResponse
from django.shortcuts import render, redirect
from django.utils.http import is_safe_url

from .models import Tweet
from .forms import TweetForm

# ALLOWED_HOSTS = settings.ALLOWED_HOSTS
BASE_API_URL = settings.BASE_API_URL



def home_view(request, *args, **kwargs):
    return render(request, "pages/feed.html", {"base_api_url": BASE_API_URL})


def tweet_create_view(request, *args, **kwargs):
    # handle authenticated user
    user = request.user
    if not request.user.is_authenticated:
        user = None
        if request.is_ajax():
            return JsonResponse({}, status=401)
        return redirect(settings.LOGIN_URL)

    form = TweetForm(request.POST or None)  # create form instance & populate with data from request
    if form.is_valid():
        data = form.save(commit=False)  # not saving, just returning the object
        data.user = user
        data.save()
        form = TweetForm()
        return JsonResponse(data.serialize(), status=201)

    if form.errors:
        return JsonResponse(form.errors, status=404)
    # return render(request, 'name.html', {'form': form})

'''
* REST API View
* Get all tweets
'''
def tweets_list_view(request, *args, **kwargs):
    query = Tweet.objects.all()  # .order_by('-id');; Now in model, there is meta for ordering
    list = [x.serialize() for x in query]
    data = { "response": list}
    return JsonResponse(data, status=200)
    # return render(request, "tweets/list.html")


def tweets_detail_view(request, tweet_id, *args, **kwargs):
    return render(request, "tweets/detail.html", context={"tweet_id": tweet_id})