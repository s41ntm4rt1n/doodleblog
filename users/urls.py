from django.conf import settings
from django.urls import path
from .views import *
from django.contrib.auth import views as auth_views
app_name='users'

urlpatterns=[

    path('accounts/signup/', Signup, name='signup'),
    path('accounts/verify-email/<slug:username>', VerifyEmail, name='verify_email'),
    path('accounts/resend-otp/', ResendOtp, name='resend_otp'),
    path('accounts/login/', Login, name='login'),
    path('accounts/logout/', Logout, name='logout'),
    
    path('accounts/password_reset/', auth_views.PasswordResetView.as_view(template_name='registration/password_reset.html', from_email=settings.EMAIL_HOST_USER, html_email_template_name='registration/password_reset_email_form.html'), name='reset_password'),
    path('accounts/password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_sent.html'), name='password_reset_done'),
    path('accounts/reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='registration/password_reset_form.html'), name='password_reset_confirm'),
    path('accounts/reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_done.html'), name='password_reset_complete'),
]