from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import ProfileUpdateForm
from .models import CustomUser, Subscription


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


@login_required
def follow_user(request, user_id):
    target_user = get_object_or_404(CustomUser, id=user_id)

    if target_user != request.user:
        Subscription.objects.get_or_create(
            subscriber=request.user,
            subscribed_user=target_user
        )

    referer_url = request.META.get('HTTP_REFERER', '/users/followers')

    if '/users/subscriptions' in referer_url:
        return redirect('subscriptions_list')
    elif '/users/followers' in referer_url:
        return redirect('followers_list')

    return redirect('followers_list')


@login_required
def unfollow_user(request, user_id):
    target_user = get_object_or_404(CustomUser, id=user_id)

    if target_user != request.user:
        Subscription.objects.filter(
            subscriber=request.user,
            subscribed_user=target_user
        ).delete()

    referer_url = request.META.get('HTTP_REFERER', '/users/followers')

    if '/users/subscriptions' in referer_url:
        return redirect('subscriptions_list')
    elif '/users/followers' in referer_url:
        return redirect('followers_list')

    return redirect('followers_list')
