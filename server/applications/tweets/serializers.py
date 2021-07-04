from rest_framework import serializers
from django.conf import settings

from .models import Tweet

MAX_LENGTH = settings.MAX_TWEET_LENGTH


class TweetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tweet
        fields = ['content']

    def validate_content(self, value):
        if len(value) > MAX_LENGTH:
            raise serializers.ValidationError("Tweet is too long...")
        return value
