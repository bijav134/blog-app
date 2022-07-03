from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE
from django.urls.base import reverse
from django.urls import reverse
from django.utils import timezone

#from django.db.models.base import Model
# Create your models here.

###################################################################################
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    prof_url = models.URLField()
    prof_pic = models.ImageField(upload_to='profile_pic/')

    def __str__(self):
        return self.user.username

###################################################################################
class Post(models.Model):
    
    author=models.ForeignKey(User, on_delete=models.CASCADE)
    title =models.CharField(max_length=50)
    text=models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    published_date =models.DateTimeField(blank=True,null=True)

    def publish(self):
        self.published_date=timezone.now()
        self.save()

    def get_absolute_url(self):
        return reverse('app:post_detail', kwargs={'pk':self.pk})

    def __str__(self):
        return self.title +' ' + self.author.username + str(self.pk)


class Comment(models.Model):
    post=models.ForeignKey(Post,on_delete=models.CASCADE,related_name='comments')
    author = models.CharField(max_length=50)
    text = models.TextField()

    def __str__(self):
        return self.author
