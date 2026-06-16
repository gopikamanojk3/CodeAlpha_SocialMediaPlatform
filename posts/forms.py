from django import forms
from .models import Post, Comment

class PostForm(forms.ModelForm):
    content = forms.CharField(widget=forms.Textarea(attrs={'rows': 3, 'placeholder': "What's on your mind?"}))
    class Meta:
        model = Post
        fields = ['content', 'image']

class CommentForm(forms.ModelForm):
    content = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Write a comment...'}))
    class Meta:
        model = Comment
        fields = ['content']
