from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import RegisterForm, UserUpdateForm, ProfileUpdateForm
from .models import Profile

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            Profile.objects.create(user=user)
            login(request, user)
            messages.success(request, 'Account created successfully!')
            return redirect('feed')
    else:
        form = RegisterForm()
    return render(request, 'users/register.html', {'form': form})

@login_required
def profile(request, username):
    user = get_object_or_404(User, username=username)
    profile = get_object_or_404(Profile, user=user)
    posts = user.post_set.all().order_by('-created_at')
    is_following = profile.followers.filter(id=request.user.id).exists()
    return render(request, 'users/profile.html', {
        'profile_user': user, 'profile': profile,
        'posts': posts, 'is_following': is_following
    })

@login_required
def edit_profile(request):
    profile, _ = Profile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'Profile updated!')
            return redirect('profile', username=request.user.username)
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=profile)
    return render(request, 'users/edit_profile.html', {'u_form': u_form, 'p_form': p_form})

@login_required
def follow_toggle(request, username):
    target_user = get_object_or_404(User, username=username)
    profile = get_object_or_404(Profile, user=target_user)
    if request.user != target_user:
        if profile.followers.filter(id=request.user.id).exists():
            profile.followers.remove(request.user)
        else:
            profile.followers.add(request.user)
    return redirect('profile', username=username)
