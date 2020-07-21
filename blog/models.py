from django.db import models
from django.utils import timezone
from django.urls import reverse
# Create your models here.

class Post(models.Model):
    author = models.ForeignKey('auth.user',on_delete=models.CASCADE)
    title = models.CharField(max_length=256)
    text = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    date_posted = models.DateTimeField(blank=True,null=True)

    group = models.ForeignKey("blog.Mygroup", related_name=("posts"), on_delete=models.CASCADE,null=True,blank=True)

    def published(self):
        self.date_posted = timezone.localtime(timezone.now())
        self.save()
    
    def approved_comments(self):
        return self.comments.filter(approved_comment=True)

    def get_absolute_url(self):
        return reverse("blog:postdetail", kwargs={"pk": self.pk})
    

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey("blog.Post",related_name='comments',on_delete=models.CASCADE)
    text = models.TextField()
    approved_comment = models.BooleanField(default=False)
    author = models.CharField(max_length=200)
    date_created = models.DateTimeField(auto_now_add=True)
    
    def approve(self):
        self.approved_comment(default=True)
        self.save()
    
    def get_absolute_url(self):
        return reverse("blog:postlist")
    
    def __str__(self):
        return self.text
        
class Mygroup(models.Model):
    name = models.CharField(max_length=256)
    admin = models.ForeignKey("auth.user", related_name='mygroups', on_delete=models.CASCADE)
    member = models.ManyToManyField("auth.user")    

    def __str__(self):
        return self.name
    
    
