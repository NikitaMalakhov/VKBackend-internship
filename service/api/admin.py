from django.contrib import admin
from .models import Friendship, User, FriendshipRequest

admin.site.register(Friendship)
admin.site.register(User)
admin.site.register(FriendshipRequest)

