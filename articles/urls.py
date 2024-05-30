from django.conf import settings
from django.urls import path
from .views import *
from . import views
from users.views import *
from django.contrib.auth import views as auth_views

urlpatterns=[
    # path('article/<slug:article_slug>/add/', ArticleCreateView.as_view(), name='create_new_article'),
    path('', OverView.as_view(), name='index'),
    path('blog/', HomeView.as_view(), name='home'),
    path('assets/', assets, name='assets'),
    path('articles/', ArticleListView.as_view(), name='articles'),
    path('author/<slug:author_slug>/', AuthorView.as_view(), name='author'),
    path('category/add/', new_category, name='new_category'),
    path('category/<slug:category_slug>/', CategoryDetailView.as_view(), name='category'),
    path('category/<slug:category_slug>/articles/', CategoryArticles.as_view(), name='category_articles'),
    path('category/<slug:category_slug>/edit/', update_category, name='update_category'),
    path('category/<slug:category_slug>/delete/', delete_category, name='delete_category'),
    path('search/', SearchView.as_view(), name='search'),
    path('article/add/', new_article, name='new_article'),
    path('article/<slug:article_slug>/edit/', update_article, name='update_article'),
    path('article/<slug:article_slug>/delete/', delete_article, name='delete_article'),
    path('article/<slug:article_slug>/', ArticleDetailView.as_view(), name='article'),
    path('blog/<slug:article_slug>/', ArticleView.as_view(), name='post'),
    
    path('categories/', CategoryListView.as_view(), name='categories'),
    
    path('asset/add/', new_asset, name='new_asset'),
    path('acounts/user/add/', new_user, name='new_user'),
    
    path('acounts/user/<slug:slug>/', user, name='user'),
    path('acounts/user/<slug:slug>/edit/', edit_user, name='edit_user'),
    path('acounts/user/<slug:slug>/image/delete', delete_user_image, name='delete_user_image'),
    path('members/', Members.as_view(), name='members'),
    path('reports/', reports, name='reports'),
    
    path('accounts/signup/', Signup, name='signup'),
    path('accounts/verify-email/<slug:username>', VerifyEmail, name='verify_email'),
    path('accounts/change-email/<slug:slug>', ChangeEmail, name='change_email'),
    path('accounts/resend-otp/', ResendOtp, name='resend_otp'),
    path('accounts/login/', Login, name='login'),
    path('accounts/logout/', Logout, name='logout'),
    path('accounts/change-password/', CustomPasswordChangeView.as_view(), name='change_password'),
    path('accounts/password_reset/', auth_views.PasswordResetView.as_view(template_name='registration/password-reset.html', from_email=settings.EMAIL_HOST_USER, html_email_template_name='registration/password_reset_email_form.html'), name='reset_password'),
    path('accounts/password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_sent.html'), name='password_reset_done'),
    path('accounts/reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='registration/password_reset_form.html'), name='password_reset_confirm'),
    path('accounts/reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_done.html'), name='password_reset_complete'),
] 