# from .forms import NewsLetterSubscriptionForm
from .models import *
from django.shortcuts import get_object_or_404

# def cart_items_count(request):
#     if request.user.is_authenticated:
#         customer=get_object_or_404(Customer, user=request.user)
#         cart = Cart.objects.filter(user=customer, ordered=False).first()
#         if cart:
#             return {'cart_items_count': cart.get_items_count}
#     return {'cart_items_count': 0}


def author_article_count(request):
    if request.user.is_authenticated:
        author=get_object_or_404(Author, user=request.user)
        articles=Article.objects.filter(author=author)
        
        if articles:
            article_count=0
            for article in articles:
                article_count+=1
            return{"article_count":article_count}
        return{"article_count":0}
    return{"article_count":0}   