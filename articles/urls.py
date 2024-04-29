from django.conf import settings
from django.urls import path
from .views import *
from . import views
from users.views import *
from django.contrib.auth import views as auth_views

urlpatterns=[
    # path('article/<slug:article_slug>/add/', ArticleCreateView.as_view(), name='create_new_article'),
    
    path('assets/', assets, name='assets'),
    path('articles/', ArticleListView.as_view(), name='articles'),
    path('author/<slug:author_slug>/', author, name='author'),
    path('category/', category, name='category'),
    path('article/add/', new_article, name='new_article'),
    path('article/<slug:article_slug>/', ArticleDetailView.as_view(), name='article'),
    path('categories/', categories, name='categories'),
    path('category/add/', new_category, name='new_category'),
    path('asset/add/', new_category, name='new_asset'),
    path('acounts/user/add/', new_category, name='new_user'),
    path('acounts/settings/', views.settings, name='settings'),
    path('acounts/user/', user, name='user'),
    path('users/', users, name='users'),
    path('reports/', reports, name='reports'),
    path('', index, name='index'),
    path('accounts/signup/', Signup, name='signup'),
    path('accounts/verify-email/<slug:username>', VerifyEmail, name='verify_email'),
    path('accounts/resend-otp/', ResendOtp, name='resend_otp'),
    path('accounts/login/', Login, name='login'),
    path('accounts/logout/', Logout, name='logout'),
    path('accounts/change-password/', CustomPasswordChangeView.as_view(), name='change_password'),
    path('accounts/password_reset/', auth_views.PasswordResetView.as_view(template_name='registration/password-reset.html', from_email=settings.EMAIL_HOST_USER, html_email_template_name='registration/password_reset_email_form.html'), name='reset_password'),
    path('accounts/password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_sent.html'), name='password_reset_done'),
    path('accounts/reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='registration/password_reset_form.html'), name='password_reset_confirm'),
    path('accounts/reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_done.html'), name='password_reset_complete'),
] 