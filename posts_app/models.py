from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
# from posts_app.models import Post

class Post(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='images/')
    create_at = models.DateTimeField(auto_now_add=True)
    data_publicacao = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'
        ordering = ['id']

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    text = models.TextField('comente:')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

class Perfil(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nome = models.CharField(max_length=100)
    bio = models.TextField(default="Bem-vindo ao meu perfil")
    image = models.ImageField(upload_to='profile_images/', default='profile_images/default.jpg')
    

    def __str__(self):
        return self.user.username
    


    


    
