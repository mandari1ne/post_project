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
    elif f'/users/profile/{user_id}/' in referer_url:
        return redirect('user_profile', user_id=target_user.id)

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
    elif f'/users/profile/{user_id}/' in referer_url:
        return redirect('user_profile', user_id=target_user.id)

    return redirect('followers_list')


def view_user_profile(request, user_id):
    target_user = get_object_or_404(CustomUser, id=user_id)

    followers = target_user.followers.all()
    subscriptions = target_user.subscriptions.all()

    is_following = False
    if request.user.is_authenticated:
        is_following = target_user in request.user.subscriptions.all()

    referer = request.META.get('HTTP_REFERER', '/users/')

    # if '/posts/' in referer:
    #     return redirect('post_index')


    context = {
        'target_user': target_user,
        'followers': followers,
        'subscriptions': subscriptions,
        'is_following': is_following,
        'referer': referer,
    }

    return render(request, 'user_profile.html', context)
