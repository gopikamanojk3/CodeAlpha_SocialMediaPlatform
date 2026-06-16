from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    avatar = models.ImageField(upload_to='avatars/', default='avatars/default.png', blank=True)
    followers = models.ManyToManyField(User, related_name='following', blank=True)

    def __str__(self):
        return f'{self.user.username} Profile'

    def follower_count(self):
        return self.followers.count()

    def following_count(self):
        return Profile.objects.filter(followers=self.user).count()
