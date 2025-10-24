from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from .models import Like

@login_required
def dashboard(request):
    users = User.objects.exclude(id=request.user.id)
    return render(request, 'crimsonmatch/dashboard.html', {'users': users})

@login_required
def like_user(request, user_id):
    liked_user = get_object_or_404(User, id=user_id)
    Like.objects.get_or_create(liker=request.user, liked=liked_user)
    return redirect('dashboard')

@login_required
def matches(request):
    liked = Like.objects.filter(liker=request.user).values_list('liked_id', flat=True)
    mutuals = Like.objects.filter(liker_id__in=liked, liked=request.user)
    matches = User.objects.filter(id__in=[m.liker_id for m in mutuals])
    return render(request, 'crimsonmatch/matches.html', {'matches': matches})
