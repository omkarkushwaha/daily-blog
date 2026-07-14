from django.db import models
from django.contrib.auth.models import User

# Create your models 
class Category(models.Model):

    name = models.CharField(
        max_length=100,
        unique=True
    )

    def __str__(self):

        return self.name
    
class Tag(models.Model):

    name = models.CharField(
        max_length=100,
        unique=True
    )

    def __str__(self):

        return self.name

class Post(models.Model):
    author = models.ForeignKey(User,on_delete=models.CASCADE)
    category = models.ForeignKey(Category,on_delete=models.SET_NULL,null=True,blank=True)
    tags = models.ManyToManyField(Tag,blank=True)
    title=models.CharField(max_length=200)
    content=models.TextField()
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to="blog_images/",blank=True,null=True)
    
    def __str__(self):
        return self.title
    

    
class Comment(models.Model):

    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    text = models.TextField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        return self.text[:20]