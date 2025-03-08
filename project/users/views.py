from django.shortcuts import render, redirect
from django.contrib.auth import logout
from .models import CustomUser

# Create your views here.

def user_index(request):
    user = request.user

    subscriptions = user.subscriptions.all()

    followers = user.followers.all()

    return render(request, 'users_index.html', {
        'user': user,
        'subscriptions': subscriptions,
        'followers': followers,
    })
