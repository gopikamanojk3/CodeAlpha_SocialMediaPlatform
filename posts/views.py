from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Post, Comment
from .forms import PostForm, CommentForm
from users.models import Profile

@login_required
def feed(request):
    Profile.objects.get_or_create(user=request.user)
    following_users = request.user.following.values_list('user', flat=True)
    posts = Post.objects.filter(author__in=[*following_users, request.user.id])
    if not posts.exists():
        posts = Post.objects.all()
    form = PostForm()
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            messages.success(request, 'Post created!')
            return redirect('feed')
    return render(request, 'posts/feed.html', {'posts': posts, 'form': form})

@login_required
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comments = post.comments.all()
    form = CommentForm()
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect('post_detail', pk=pk)
    return render(request, 'posts/post_detail.html', {'post': post, 'comments': comments, 'form': form})

@login_required
def like_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)
    return redirect(request.META.get('HTTP_REFERER', 'feed'))

@login_required
def delete_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if post.author == request.user:
        post.delete()
        messages.success(request, 'Post deleted.')
    return redirect('feed')
