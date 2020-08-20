from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField

class Author(models.Model):
    name=models.ForeignKey(User,on_delete=models.CASCADE)
    profile_picture=models.FileField()
    details=models.TextField()

    def __str__(self):
        return self.name.username

class Category(models.Model):
    name=models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Article(models.Model):
    article_author=models.ForeignKey(Author,on_delete=models.CASCADE)
    title=models.CharField(max_length=100)
    body=RichTextUploadingField()
    image=models.FileField()
    posted_on=models.DateTimeField(auto_now_add=True ,auto_now=False)
    updated_on=models.DateTimeField(auto_now_add=False,auto_now=True)
    category=models.ForeignKey(Category,on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def get_single_url(self):
        return reverse('blog:single_post',kwargs={'id':self.id})
    def get_author_url(self):
        return reverse('blog:author',kwargs={'name':self.article_author.name.username})

class Comment(models.Model):
    post=models.ForeignKey(Article,on_delete=models.CASCADE)
    post_comment=models.TextField()

    def __str__(self):
        return self.post.title


