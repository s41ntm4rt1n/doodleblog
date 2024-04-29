from django.db import models
from django.contrib.auth.models import User
import os
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.utils.text import slugify
from django.utils.html import format_html
from django.utils.safestring import SafeText
from django.conf import settings
import random
import string
from decimal import Decimal 
from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.conf import settings

class Category(models.Model):
    title=models.CharField(max_length=255, blank=True)
    slug=models.SlugField(unique=True, blank=False)
    
    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ('title',)
        verbose_name_plural = 'Categories'


    # def get_absolute_url(self):
    #     return reverse('articles:category', kwargs={
    #         'category_slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

class Member(models.Model):
    user=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='members')
    name=models.CharField(max_length=255, blank=True)
    image=models.ImageField(upload_to='users', blank=True)
    slug=models.SlugField(unique=True, blank=False)
    is_author=models.BooleanField(default=False)
    is_moderator=models.BooleanField(default=False)
    
    def __str__(self):
        return self.name
    
    # def get_absolute_url(self):
    #     return reverse('articles:author', kwargs={
    #         'author_slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

class Moderator(models.Model):
    member=models.ForeignKey(Member, on_delete=models.CASCADE, related_name='moderators')
    is_moderator=models.BooleanField(default=True)

    def __str__(self):
        return f"{self.member.name}"
        
def author_images_upload(instance, filename):
    author_name = instance.author.name
    return os.path.join("authors", author_name, filename)


class Author(models.Model):
    user=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='authors')
    name=models.CharField(max_length=255, blank=True)
    image=models.ImageField(upload_to=author_images_upload, blank=True)
    slug=models.SlugField(unique=True, blank=False)
    is_author=models.BooleanField(default=True)
    
    def __str__(self):
        return self.name
    
    # def get_absolute_url(self):
    #     return reverse('articles:author', kwargs={
    #         'author_slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
        
    def get_articles(self):
        articles=Article.objects.filter(author=self)
        return articles
    
    @property
    def get_articles_count(self):
        return self.article_set.count()
  
def article_images_upload(instance, filename):
    article_name = instance.title 
    return os.path.join("articles", article_name, filename)
        
class Article(models.Model):
    category=models.ForeignKey(Category, on_delete=models.CASCADE, blank=True)
    author=models.ForeignKey(Author, on_delete=models.CASCADE, null=True)
    title=models.CharField(max_length=255, blank=True)
    body=models.TextField(blank=True)
    featured_image=models.ImageField(upload_to=article_images_upload, blank=True)
    created_at=models.DateTimeField(auto_now_add=True)
    status=models.CharField(
        max_length=20,
        choices=[
            ('Draft','Draft'),
            ('Published' , 'Published'),
        ],
        default='Draft',
    )
    updated_at=models.DateTimeField(auto_now=True, blank=True)
    slug=models.SlugField(unique=True, blank=False)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
        
    def formatted_body(self):
        return format_html(SafeText(self.body))
    
class Comment(models.Model):
    article=models.ForeignKey(Article, on_delete=models.CASCADE, blank=True)
    commenter=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='commenters')
    comment=models.TextField(blank=True)
    created_at=models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.commenter