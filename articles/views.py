from typing import Any
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from articles.models import *  
from articles.forms import ArticleCreateForm
from django.utils import timezone

   

def index(request):
    return render(request, 'index.html')

def article(request):
    return render(request, 'article.html')

class ArticleListView(ListView):
    model= Article
    template_name='articles.html'
    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['articles']=Article.objects.all()
        return context

class ArticleDetailView(DetailView):
    model= Article
    template_name='article.html'
    
    def get_object(self, queryset=None):
        article_slug = self.kwargs['article_slug']
        article = get_object_or_404(Article, slug=article_slug)
        return article
    
class ArticleCreateView(CreateView):
    model=Article
    template_name='new-article.html'
    
    # def get_object(self, queryset=None):
    #     article_slug = self.kwargs['article_slug']
    #     article = get_object_or_404(Article, slug=article_slug)
    #     return article

def new_article(request):
    author=get_object_or_404(Author,  user=request.user)
    if request.method == 'POST':
        form = ArticleCreateForm(request.POST)
        if form.is_valid():
            new_article = form.save(commit=False)
            new_article.author = author  
            new_article.save()
            return redirect('articles')
    else:
        form = ArticleCreateForm()
        context={
            'form': form,
            'author': author,
        }
    return render(request, 'new-article.html', context)    

    
def assets(request):
    return render(request, 'assets.html')

def new_asset(request):
    return render(request, 'new-asset.html')

def articles(request):
    return render(request, 'articles.html')

def author(request, author_slug):
    author=get_object_or_404(Author, slug=author_slug)
    context={
        'author' : author,
    }
    return render(request, 'author.html', context)

def category(request):
    return render(request, 'category.html')

def categories(request):
    return render(request, 'categories.html')



def new_category(request):
    return render(request, 'new-category.html')

def settings(request):
    return render(request, 'settings.html')

def user(request):
    return render(request, 'user.html')
def new_user(request):
    return render(request, 'new-user.html')
def users(request):
    return render(request, 'users.html')

def reports(request):
    return render(request, 'reports.html')
