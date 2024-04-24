from django.db.models.signals import post_save
from django.conf import settings
from django.dispatch import receiver
from users.models import OTPToken
from django.core.mail import EmailMessage
from django.utils import timezone
from django.template.loader import render_to_string

@receiver(post_save, sender=settings.AUTH_USER_MODEL) 
def create_token(sender, instance, created, **kwargs):
    if created:
        if instance.is_superuser:
            pass
        else:
            OTPToken.objects.create(user=instance, expires_at=timezone.now() + timezone.timedelta(minutes=10))
            instance.is_active=False 
            instance.save()
        # email credentials
        otp = OTPToken.objects.filter(user=instance).last()       
        subject="Email Verification"
        context = {
            'username': instance.username,
            'otp': otp.otp_code ,
        }
        html_content = render_to_string('registration/verify_email_form.html', context)
        email = EmailMessage(
            subject,
            html_content,
            'MS_AIFmlp@robotsaint.com',  
            [instance.email]  
        )
        email.content_subtype = "html"  
        email.send()
        
        