from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.db.models import Q
from django.contrib import messages
from .models import Like, MatchNotification


@login_required
def dashboard(request):
    """
    Show all users except the logged-in user.
    Optional search query for filtering users.
    """
    query = request.GET.get('q', '')
    users = User.objects.exclude(id=request.user.id)

    if query:
        users = users.filter(
            Q(username__icontains=query) |
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query)
        )

    liked_users = Like.objects.filter(liker=request.user).values_list('liked_id', flat=True)

    return render(request, 'crimsonmatch/dashboard.html', {
        'users': users,
        'liked_users': liked_users,
        'query': query
    })


@login_required
def profile_view(request, user_id):
    """
    View another user's profile.
    """
    user_profile = get_object_or_404(User, id=user_id)
    has_liked = Like.objects.filter(liker=request.user, liked=user_profile).exists()
    return render(request, 'crimsonmatch/profile.html', {
        'user_profile': user_profile,
        'has_liked': has_liked
    })


@login_required
def like_user(request, user_id):
    """
    Like another user. If both users liked each other, create a match notification.
    """
    liked_user = get_object_or_404(User, id=user_id)

    if liked_user == request.user:
        messages.warning(request, "You can't like yourself!")
        return redirect('dashboard')

    like, created = Like.objects.get_or_create(liker=request.user, liked=liked_user)

    if created:
        # Check for mutual like
        if Like.objects.filter(liker=liked_user, liked=request.user).exists():
            MatchNotification.objects.get_or_create(
                user=request.user,
                matched_with=liked_user
            )
            MatchNotification.objects.get_or_create(
                user=liked_user,
                matched_with=request.user
            )
            messages.success(request, f"You and {liked_user.username} are now a matc_
