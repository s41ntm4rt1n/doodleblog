# from .forms import NewsLetterSubscriptionForm
from .models import *
from django.shortcuts import get_object_or_404
from .forms import *

def articles_count(request):
    articles=Article.objects.all()
    if articles:
        article_count=0
        for article in articles:
            article_count+=1
        return{"article_count":article_count}
    return{"article_count":0}
            
def members_count(request):
    members=Member.objects.all()
    if members:
        member_count=0
        for member in members:
            member_count+=1
        return{"member_count":member_count}
    return{"member_count":0}
            
def categories_count(request):
    categories=Category.objects.all()
    if categories:
        category_count=0
        for category in categories:
            category_count+=1
        return{"category_count":category_count}
    return{"category_count":0}

def credentials(request):
    if request.user.is_authenticated:
        try:
            member= get_object_or_404(Member, user=request.user)
        except Member.DoesNotExist:
            member = None

        return {'member': member}
    member = None
    return {'member': member}


def article_search_form(request):
    return {'article_search_form': ArticleSearchForm()}