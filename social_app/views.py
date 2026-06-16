from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import JsonResponse
from .models import Profile, Post, Comment
from .forms import UserRegisterForm, PostForm, CommentForm, ProfileForm
from django.db.models import Q


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            Profile.objects.create(user=user)
            login(request, user)
            messages.success(request, 'Account created successfully!')
            return redirect('home')
    else:
        form = UserRegisterForm()
    return render(request, 'social_app/register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid credentials.')
    return render(request, 'social_app/login.html')


@login_required
def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def home(request):
    following_users = request.user.profile.following.values_list('user', flat=True)
    posts = Post.objects.filter(
        Q(author__in=following_users) | Q(author=request.user)
    ).select_related('author', 'author__profile').prefetch_related('likes', 'comments')
    form = PostForm()
    return render(request, 'social_app/home.html', {'posts': posts, 'form': form})


@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            messages.success(request, 'Post created!')
    return redirect('home')


@login_required
def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.user in post.likes.all():
        post.likes.remove(request.user)
        liked = False
    else:
        post.likes.add(request.user)
        liked = True
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'liked': liked, 'count': post.get_likes_count()})
    return redirect('home')


@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
    return redirect('post_detail', post_id=post_id)


@login_required
def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    comments = post.comments.select_related('author')
    form = CommentForm()
    return render(request, 'social_app/post_detail.html', {'post': post, 'comments': comments, 'form': form})


@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id, author=request.user)
    post.delete()
    messages.success(request, 'Post deleted.')
    return redirect('home')


@login_required
def profile(request, username):
    user = get_object_or_404(User, username=username)
    profile_obj, _ = Profile.objects.get_or_create(user=user)
    posts = Post.objects.filter(author=user).select_related('author')
    is_following = request.user.profile.following.filter(user=user).exists()
    return render(request, 'social_app/profile.html', {
        'profile_user': user,
        'profile_obj': profile_obj,
        'posts': posts,
        'is_following': is_following,
    })


@login_required
def edit_profile(request):
    profile_obj, _ = Profile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile_obj)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated!')
            return redirect('profile', username=request.user.username)
    else:
        form = ProfileForm(instance=profile_obj)
    return render(request, 'social_app/edit_profile.html', {'form': form})


@login_required
def follow_user(request, username):
    target_user = get_object_or_404(User, username=username)
    target_profile, _ = Profile.objects.get_or_create(user=target_user)
    my_profile, _ = Profile.objects.get_or_create(user=request.user)
    if target_user != request.user:
        if my_profile.following.filter(user=target_user).exists():
            my_profile.following.remove(target_profile)
        else:
            my_profile.following.add(target_profile)
    return redirect('profile', username=username)


@login_required
def explore(request):
    query = request.GET.get('q', '')
    users = []
    posts = Post.objects.all().select_related('author', 'author__profile')
    if query:
        users = User.objects.filter(
            Q(username__icontains=query) | Q(first_name__icontains=query)
        ).exclude(id=request.user.id)
        posts = posts.filter(content__icontains=query)
    return render(request, 'social_app/explore.html', {'users': users, 'posts': posts, 'query': query})
