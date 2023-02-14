from email.policy import default
from django.db import models
from django.contrib.auth.models import User

# Create your models here.

# Contentに紐付けるカテゴリー
class Category(models.Model):
    name = models.CharField(
        max_length=30,
        verbose_name='カテゴリ名',
        blank=True,
        null=True)

    def __str__(self):
        return self.name

class Content(models.Model):
    title = models.CharField(max_length=140)
    # blurがかかった単語
    blur_word = models.CharField(max_length=140)
    # blurのかかっていない単語
    word = models.CharField(max_length=140)
    content = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, verbose_name=("カテゴリ名"), on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.title

