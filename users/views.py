from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from .models import *
from django.template.loader import render_to_string
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.core.mail import send_mail, EmailMessage
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from articles.forms import CustomPasswordChangeForm
from articles.models import Member
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
from articles.forms import CustomPasswordChangeForm

class CustomPasswordChangeView(auth_views.PasswordChangeView):
    form_class = CustomPasswordChangeForm
    template_name = 'registration/password.html'
    success_url = reverse_lazy('index')

def Signup(request):
    if request.method == 'POST':
        first_name = request.POST['FirstName']
        last_name = request.POST['LastName']
        email = request.POST['Email']
        username = request.POST['Username']
        password1 = request.POST['Password1']
        password2 = request.POST['Password2']

        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return redirect('signup')

        if len(username) > 15:
            messages.error(request, "Username is too long.")
            return redirect('signup')

        try:
            existing_username = get_user_model().objects.filter(username=username).first()
            if existing_username:
                messages.error(request, "Username already exists. Please choose a different username.")
                return redirect('signup')
            
            existing_email = get_user_model().objects.filter(email=email).first()
            if existing_email:
                messages.error(request, "Email already exists. Please use a different email.")
                return redirect('signup')
            
            user = get_user_model().objects.create_user(username=username, password=password1, email=email, first_name=first_name, last_name=last_name, is_active=False)
            member=Member.objects.create(user=user, name=f'{first_name} {last_name}')
                        
            messages.success(request, "Your account has been created successfully. An OTP was sent to your email.")
            return redirect('verify_email', username=username)
        except ValidationError as e:
            messages.error(request, e.message_dict)
            return redirect('signup')

    return render(request, 'registration/signup.html')


def VerifyEmail(request, username):
    user=get_user_model().objects.get(username=username)
    user_otp=OTPToken.objects.filter(user=user).last()
    
    if request.method == 'POST':
        if user_otp.otp_code == request.POST['otp_code']:
            # checking for expired token
            if user_otp.expires_at > timezone.now():
                user.is_active=True
                user.save()
                messages.success(request, "Account activated successfully!! You can Login.")
                return redirect("login")
            
            # expired token
            else:
                messages.error(request, "The OTP has expired, get a new OTP!")
                return redirect("verify_email", username=user.username)

        # invalid otp code
        else:
            messages.error(request, "Invalid OTP entered, enter a valid OTP!")
            return redirect("verify_email", username=user.username)
        
    context = {}
    return render(request, "registration/verifyemail.html", context)

@login_required    
def ChangeEmail(request, slug):
    # user inputs new email
    # the registered user model is fetched and email changed
    # user is redirected to email verification
    if request.user.is_authenticated:
        if request.method == 'POST':
            user_email = request.POST["email"]
            
            if get_user_model().objects.filter(username=slug).exists():
                user = get_user_model().objects.get(username=slug)
                user.email=user_email
                user.save()
                
                otp = OTPToken.objects.create(user=user, expires_at=timezone.now() + timezone.timedelta(minutes=10))
                # email variables
                subject="Resend OTP"
                context = {
                'username': user.username,
                'otp': otp.otp_code ,
                }
                html_content = render_to_string('registration/otp.html', context)
                email = EmailMessage(
                    subject,
                    html_content,
                    'MS_AIFmlp@robotsaint.com',
                    [user.email]
                )
                email.content_subtype = "html"
                email.send()
                    
                messages.success(request, "An OTP has been sent to your new email address")
                return redirect("verify_email", username=user.username)
    context = {}
    return render(request, "users/change-email.html", context)
                
        
def ResendOtp(request):
    if request.method == 'POST':
        user_email = request.POST["Email"]
        
        if get_user_model().objects.filter(email=user_email).exists():
            user = get_user_model().objects.get(email=user_email)
            otp = OTPToken.objects.create(user=user, expires_at=timezone.now() + timezone.timedelta(minutes=10))
            # email variables
            subject="Resend OTP"
            context = {
            'username': user.username,
            'otp': otp.otp_code ,
            }
            html_content = render_to_string('registration/otp.html', context)
            email = EmailMessage(
                subject,
                html_content,
                'MS_AIFmlp@robotsaint.com',
                [user.email]
            )
            email.content_subtype = "html"
            email.send()
                
            messages.success(request, "A new OTP has been sent to your email address")
            return redirect("verify_email", username=user.username)

        else:
            messages.error(request, "This email is not linked to any user")
            return redirect("resend_otp")
        
           
    context = {}
    return render(request, "registration/resendotp.html", context)

def Login(request):
    if request.method == 'POST':
        email = request.POST['Email']
        password = request.POST['Password1']
        
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "You have been loged in successfully!")
            return redirect('index')
        else:
            messages.error(request, "Incorrect email or password!")
            return redirect('login') 
    else:
        return render(request, "registration/login.html")

@login_required
def Logout(request):
    logout(request)
    messages.error(request, 'You have been logged out!')
    return redirect('index')