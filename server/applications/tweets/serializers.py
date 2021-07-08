from rest_framework import serializers
from django.conf import settings

from .models import Tweet

MAX_LENGTH = settings.MAX_TWEET_LENGTH
TWEET_ACTION_OPTIONS = settings.TWEET_ACTION_OPTIONS


class TweetActionSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    action = serializers.CharField()
    content = serializers.CharField(allow_blank=True, required=False)

    def validate_action(self, value):
        value = value.lower().strip()  # "Like " -> "like"
        if not value in TWEET_ACTION_OPTIONS:
            raise serializers.ValidationError("This is not a valid action for tweets")
        return value


class TweetCreateSerializer(serializers.ModelSerializer):
    # user = PublicProfileSerializer(source='user.profile', read_only=True)  # serializers.SerializerMethodField(read_only=True)
    likes = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Tweet
        fields = ['id', 'content', 'likes', 'timestamp'] # 'user',

    def validate_content(self, value):
        if len(value) > MAX_LENGTH:
            raise serializers.ValidationError("Tweet is too long...")
        return value

    def get_likes(self, obj):
        return obj.likes.count()


class TweetSerializer(serializers.ModelSerializer):
    # user = PublicProfileSerializer(source='user.profile', read_only=True)
    likes = serializers.SerializerMethodField(read_only=True)
    # is_retweet = serializers.SerializerMethodField(read_only=True) this is not needed, because we have property used
    parent = TweetCreateSerializer(read_only=True)

    class Meta:
        model = Tweet
        fields = [ 'id', 'content', 'likes', 'is_retweet', 'parent', 'timestamp'] # 'user',

    def get_likes(self, obj):
        return obj.likes.count()
