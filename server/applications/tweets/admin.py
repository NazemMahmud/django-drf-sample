from django.contrib import admin

# Register your models here.
from .models import Tweet, TweetLike

'''
    This is for admin dashboard site
    All changes will be reflected upon base_url/admin site
'''


class TweetLikeAdmin(admin.TabularInline):
    model = TweetLike


class TweetAdmin(admin.ModelAdmin):
    inlines = [TweetLikeAdmin]
    list_display = ['__str__', 'user']
    search_fields = ['content', 'user__username', 'user__email']

    class Meta:
        model = Tweet


admin.site.register(Tweet, TweetAdmin)
