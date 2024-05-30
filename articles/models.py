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


class Category(models.Model):
    title=models.CharField(max_length=255, blank=True)
    slug=models.SlugField(unique=True, blank=False)
    
    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ('title',)
        verbose_name_plural = 'Categories'

    def articles(self):
        return Article.objects.filter(category=self)
        
    def get_article_count(self):
        articles=Article.objects.filter(category=self)
        
        if articles:
            article_count=0
            for article in articles:
                article_count+=1
            return article_count
        return 0
        
    def get_absolute_url(self):
        return reverse('category', kwargs={
            'category_slug': self.slug})

    def get_delete_url(self):
        return reverse('delete_category', kwargs={
            'category_slug': self.slug})
    
    def get_update_url(self):
        return reverse('update_category', kwargs={
            'category_slug': self.slug})
        
    def get_category_articles_url(self):
        return reverse('category_articles', kwargs={
            'category_slug': self.slug})
        
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class Member(models.Model):
    user=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='members')
    name=models.CharField(max_length=255, blank=True)
    image=models.ImageField(upload_to='users', blank=True)
    slug=models.SlugField(unique=True, blank=True)
    is_author=models.BooleanField(default=False)
    is_moderator=models.BooleanField(default=False)
    
    def __str__(self):
        return self.name
    
    def has_image(self):
        return bool(self.image)
    
    def get_absolute_url(self):
        return reverse('user', kwargs={
            'slug': self.slug})
        
    def get_edit_url(self):
        return reverse('edit_user', kwargs={
            'slug': self.slug})
    
    def get_image_delete_url(self):
        return reverse('delete_user_image', kwargs={
            'slug': self.slug})
            
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.user.username)
        super().save(*args, **kwargs)
        
        if not self.is_author:
            try:
                author = Author.objects.get(member=self)
                author.delete()
            except Author.DoesNotExist:
                pass
        if not self.is_moderator:
            try:
                moderator = Moderator.objects.get(member=self)
                moderator.delete()
            except Moderator.DoesNotExist:
                pass

class Moderator(models.Model):
    member=models.OneToOneField(Member, on_delete=models.CASCADE, related_name='moderators')
    is_moderator=models.BooleanField(default=True)

    def __str__(self):
        return f"{self.member.name}"
        
# def author_images_upload(instance, filename):
#     author_name = instance.author.name
#     return os.path.join("authors", author_name, filename)


class Author(models.Model):
    member=models.OneToOneField(Member, on_delete=models.CASCADE, related_name='authors', null=True)
    bio=models.TextField(blank=True)
    is_author=models.BooleanField(default=True)
    
    def __str__(self):
        if self.member:
            return f"{self.member.name}"
        else:
            return "Unknown Author"
    
    def get_absolute_url(self):
        return reverse('author', kwargs={
            'author_slug': self.member.slug})
        
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
    category=models.ForeignKey(Category, on_delete=models.SET_NULL, blank=True, null=True)
    author=models.ForeignKey(Author, on_delete=models.CASCADE, null=True,  blank=True)
    title=models.CharField(max_length=255, blank=True)
    body=models.TextField(blank=True)
    image=models.ImageField(upload_to=article_images_upload, blank=True)

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
    
    def __str__(self):
        return f"{self.title}"
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
        
        if self.image:
            image = Image.open(self.image)

            # Resize the image to a desired size
            max_size = (420, 360)
            image.thumbnail(max_size)

            # Prepare the content of the resized image
            img_io = BytesIO()
            image.save(img_io, format='PNG', quality=120)
            img_io.seek(0)
            image_content = ContentFile(img_io.read())

            # Determine the storage backend to use (local storage or Amazon S3)
            if self.image.storage == default_storage:
                # If using local storage, save the resized image back to the same field
                self.image.save(os.path.basename(self.image.name), image_content, save=False)
            else:
                # If using Amazon S3, create a new file with the resized image content and save it
                resized_image_name = f"{os.path.splitext(self.image.name)[0]}_resized.png"
                self.image.storage.save(resized_image_name, image_content)

            super(Article, self).save(*args, **kwargs)

        
    def formatted_body(self):
        return format_html(SafeText(self.body))
    
    def get_url(self):
        return reverse( "post", kwargs={
            'article_slug' : self.slug})

    def get_absolute_url(self):
        return reverse( "article", kwargs={
            'article_slug' : self.slug})
        
    def get_update_url(self):
        return reverse('update_article', kwargs={
            'article_slug': self.slug})
    
    def get_delete_url(self):
        return reverse('delete_article', kwargs={
            'article_slug': self.slug})
                
    @property    
    def has_image(self):
        return bool(self.image)
    
    @property
    def get_image(self):
        if self.has_image:
            return self.image.url
        return None
            


        
class Comment(models.Model):
    article=models.ForeignKey(Article, on_delete=models.CASCADE, blank=True)
    commenter=models.ForeignKey(Member, on_delete=models.CASCADE, related_name='commenters')
    comment=models.TextField(blank=True)
    created_at=models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.commenter
    
class Reply(models.Model):
    comment=models.ForeignKey(Comment, on_delete=models.CASCADE, blank=True)
    reply=models.TextField(blank=True, null=True)
    replier=models.ForeignKey(Member, on_delete=models.CASCADE, related_name='repliers')
    created_at=models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.replier
    
    class Meta:
        ordering = ('-created_at',)
        verbose_name_plural = 'Replies'
    
class Report(models.Model):
    article=models.ForeignKey(Article, on_delete=models.CASCADE, blank=True)
    shares=models.DecimalField(max_digits=10, decimal_places=1, default=0, blank=True, null=True)
    views=models.DecimalField(max_digits=10, decimal_places=1, default=0, blank=True, null=True)
    
    def __str__(self):
        return self.article

class ArticleLike(models.Model):
    article=models.ForeignKey(Article, on_delete=models.CASCADE, blank=True)
    member=models.ForeignKey(Member, on_delete=models.SET_NULL, blank=True, null=True)
    like=models.DecimalField(max_digits=10, decimal_places=1, default=0)
    
    def __str__(self):
        return self.article