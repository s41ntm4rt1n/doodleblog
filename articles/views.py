from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView, UpdateView, View
from articles.models import *  
from articles.forms import ArticleSearchForm
from django.utils import timezone
from django.conf import settings
from django.contrib.auth import get_user_model
import os   
# from markdown2 import markdown
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.views import View
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


class HomeView(ListView):
    model= Article
    template_name='blog/blog.html'
    paginate_by=6
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['articles']=Article.objects.all()
        return context


class OverView(ListView):
    model= Article
    template_name='index.html'
    paginate_by=10
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['articles']=Article.objects.all()
        return context  


class ArticleListView(ListView):
    model= Article
    template_name='articles/articles.html'
    paginate_by=10
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['articles']=Article.objects.all()
        return context

class ArticleDetailView(DetailView):
    model= Article
    template_name='articles/article.html'
    
    def get_object(self, queryset=None):
        article_slug = self.kwargs['article_slug']
        article = get_object_or_404(Article, slug=article_slug)
        
        return article
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class ArticleView(DetailView):
    model= Article
    template_name='blog/post.html'
    
    def get_object(self, queryset=None):
        article_slug = self.kwargs['article_slug']
        article = get_object_or_404(Article, slug=article_slug)
        
        return article
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
        
class ArticleCreateView(CreateView):
    model=Article
    template_name='articles/new-article.html'
    
    # def get_object(self, queryset=None):
    #     article_slug = self.kwargs['article_slug']
    #     article = get_object_or_404(Article, slug=article_slug)
    #     return article
    
def new_article(request):
    member=get_object_or_404(Member, user=request.user)
    author=get_object_or_404(Author, member=member)
    categories=Category.objects.all()
    
    if request.method == 'POST':        
        category=request.POST.get('category')
        title=request.POST.get('title')
        body=request.POST.get('body')
        image=request.FILES.get('image')
        status=request.POST.get('status')
        
        article = Article(
            title=title,
            body=body,
            status=status,
            image=image,
            
        )
        article.category=Category.objects.filter(title=category).first()
        article.author=author
        article.save()
        messages.success(request, f"Article added!")
        return redirect('articles')
    
    context={
        'author': author,
        'categories':categories,
    }
    return render(request, 'articles/new-article.html', context)    

def update_article(request, article_slug):
    article =get_object_or_404(Article, slug=article_slug)
    categories=Category.objects.all()
    if article:
        if request.method == 'POST':
            category=request.POST.get('category')
            title=request.POST.get('title')
            body=request.POST.get('body')
            image=request.FILES.get('image')
            status=request.POST.get('status')
            
            if category:
                article.category=Category.objects.filter(title=category).first()
            if title:
                article.title=title
            if body:
                article.body=body
            if image:
                article.image=image
            if status:
                article.status=status
            
            article.updated_at=timezone.now()
            article.save()
            messages.success(request, f"Article has been updated successfully")
            return redirect('article', article_slug=article.slug)
            
    context={
       'article' : article,
       'categories':categories,
    }
    return render(request, 'articles/edit-article.html', context)

def delete_article(request, article_slug):
    article =get_object_or_404(Article, slug=article_slug)
    
    if article:
        article.delete()
        messages.success(request, f"Article has been deleted successfully")
        return redirect('articles')
    
# class SearchView(View):
#     template_name = 'blog/search.html'
#     paginate_by = 2
    
#     def get(self, request, *args, **kwargs):
#         form = ArticleSearchForm(request.GET)
#         results = []
#         if form.is_valid():
#             query = form.cleaned_data['query']
#             results = Article.objects.filter(
#                 Q(title__icontains=query) | Q(body__icontains=query) |
#                 Q(category__icontains=query)
#             ).distinct()

#             results = list(results)  

#         context = {
#             'query' : query,
#             'form': form,
#             'results' : results,
#         }
#         return render(request, self.template_name, context)
    
class SearchView(View):
    template_name = 'blog/search.html'
    paginate_by = 4
    
    def get(self, request):
        query = request.GET.get('q', '')
        results = self.search_articles(query)
        # item_count = results.count()
        print(results)
        page = request.GET.get('page', 1)
        paginator = Paginator(results, self.paginate_by)
        try:
            paginated_results = paginator.page(page)
        except PageNotAnInteger:
            paginated_results = paginator.page(1)
        except EmptyPage:
            paginated_results = paginator.page(paginator.num_pages)

        context = {
            'results': paginated_results,
            'query': query,
        }
        return render(request, self.template_name, context)
    

    def search_articles(self, query):
        if query:
            results = []
            resultsintitle=Article.objects.filter(title__icontains=query).distinct()
            resutsinbody=Article.objects.filter(body__icontains=query).distinct()
            results=list(resultsintitle)  + list(resutsinbody)
            
            return results
        else:
            return Article.objects.none()
    
def assets(request):
    return render(request, 'assets/assets.html')

def new_asset(request):
    return render(request, 'assets/new-asset.html')

class AuthorView(ListView):
    model= Article
    template_name='users/author.html'
    context_object_name='articles'
    paginate_by=10
    
    def get_object(self, queryset=None):
        author_slug = self.kwargs['author_slug']
        member=get_object_or_404(Member, slug=author_slug)
        author=get_object_or_404(Author, member=member)
        return author
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        author_slug = self.kwargs['author_slug']
        member=get_object_or_404(Member, slug=author_slug)
        author=get_object_or_404(Author, member=member)
        context['author']=author
        return context

    def get_queryset(self):
        author_slug = self.kwargs['author_slug']
        member=get_object_or_404(Member, slug=author_slug)
        author=get_object_or_404(Author, member=member)
        return author.get_articles()
    
#CATEGORIES

class CategoryListView(ListView):
    model= Category
    template_name='articles/categories.html'
    paginate_by=6
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories']=Category.objects.all()
        return context

class CategoryDetailView(ListView):
    model= Article
    template_name='articles/category.html'
    context_object_name='articles'
    paginate_by=10
    
    def get_object(self, queryset=None):
        category_slug = self.kwargs['category_slug']
        category = get_object_or_404(Category, slug=category_slug)
        return category
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_slug = self.kwargs['category_slug']
        category = get_object_or_404(Category, slug=category_slug)
        context['category']=category
        return context

    def get_queryset(self):
        category_slug = self.kwargs['category_slug']
        category = get_object_or_404(Category, slug=category_slug)
        return category.articles()

class CategoryArticles(ListView):
    model= Article
    template_name='articles/category-articles.html'
    context_object_name='articles'
    paginate_by=10
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_slug = self.kwargs['category_slug']
        category = get_object_or_404(Category, slug=category_slug)
        context['category']=category
        return context
    
    def get_queryset(self):
        category_slug = self.kwargs['category_slug']
        category = get_object_or_404(Category, slug=category_slug)
        return category.articles()
    
def update_category(request, category_slug):
    category=Category.objects.filter(slug=category_slug).first()
    if request.method == 'POST':
        title=request.POST.get('title')
    
        category.title=title
        category.save()
        messages.success(request, f"Category '{category.title}' has been updated successfully")
        return redirect('categories')
    context={
        'category': category,
    }
    return render(request, 'articles/edit-category.html', context)

def new_category(request):
    if request.method == 'POST':
        title=request.POST.get('title')
        
        category=Category.objects.create(
            title=title,
        )
        category.save()
        messages.success(request, f"Category '{category.title}' has been added successfully") 
        return redirect('categories')
    return render(request, 'articles/new-category.html')

def delete_category(request, category_slug):
    category=Category.objects.filter(slug=category_slug).first()
    
    category.delete()
    messages.success(request, f"Category '{category.title}' has been deleted successfully") 
    return redirect('categories')
    
def category_articles(request, category_slug):
    category=get_object_or_404(Category, slug=category_slug)
    articles=Article.objects.filter(category=category)
    
    return render(request, 'articles/category-articles.html', {'articles':articles, 'category': category})

def new_user(request):
    return render(request, 'users/new-user.html')

@login_required
def edit_user(request, slug):
    member=get_object_or_404(Member, slug=slug)
    if request.method == 'POST':
        image=request.FILES.get('image')
        name=request.POST.get('name')
        
        if image:
            member.image=image
        if name:    
            member.name=name
        member.save()
        return redirect('user', slug=member.slug)
    context={
        'member': member,
    }
    return render(request, 'users/edit-user.html', context)

@login_required
def delete_user_image(request, slug):
    member=get_object_or_404(Member, slug=slug)
    member.image.delete()
    return redirect('user', slug=member.slug)

@login_required
def user(request, slug):
    member=get_object_or_404(Member, slug=slug)
    context={
        'member': member,
    }
    return render(request, 'users/user.html', context)

class Members(ListView):
    model=Member
    template_name='users/users.html'
    context_object_name='members'
    paginate_by=10
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['members']=Member.objects.all()
        return context

    
def reports(request):
    return render(request, 'reports.html')
