from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import ProfileUpdateForm
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

@login_required
def edit_profile(request):
    if request.method == 'POST':

        form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user)

        if form.is_valid():
            form.save()
            return redirect('/users/')
    else:
        form = ProfileUpdateForm(instance=request.user)

    return render(request, 'edit_profile.html', {'form': form})

@login_required
def user_followers(request):
    user = request.user
    followers = user.followers.all()

    return render(request, 'followers_list.html', {'followers': followers})

@login_required
def user_subscriptions(request):
    user = request.user
    subscriptions = user.subscriptions.all()

    return render(request, 'subscriptions_list.html', {'subscriptions': subscriptions})


