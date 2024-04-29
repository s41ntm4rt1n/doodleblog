from django import forms
from .models import *
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash

class ArticleCreateForm(forms.ModelForm):
    class Meta:
        model=Article
        fields = ['category', 'author', 'title', 'body', 'featured_image', 'status']
        # widgets = {
        #     'category': forms.Select(attrs={'class': 'input-text', 'id': 'category'}),
        #     'author': forms.TextInput(attrs={'class': 'input-text', 'id': 'author'}),
        #     'title': forms.TextInput(attrs={'class': 'input-text', 'id': 'title'}),
        #     'body': forms.Textarea(attrs={'class': 'input-textarea', 'id': 'body'}),
        #     'featured_image': forms.FileInput(attrs={'class': 'input-file', 'id': 'featured_image'}),
        #     'status': forms.Select(attrs={'class': 'input-select', 'id': 'status'}),
        # }
class CustomPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(
        label='Old Password',
        widget=forms.PasswordInput(attrs={'class': 'yx-n_x form-control yx-me js-password__input'})
    )
    new_password1 = forms.CharField(
        label='New Password',
        widget=forms.PasswordInput(attrs={'class': 'yx-n_x form-control yx-me js-password__input'})
    )
    new_password2 = forms.CharField(
        label='Confirm New Password',
        widget=forms.PasswordInput(attrs={'class': 'yx-n_x form-control yx-me js-password__input'})
    )

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["new_password1"])
        if commit:
            user.save()
            # Update the user's session to prevent them from being logged out
            update_session_auth_hash(self.request, user)
        return user
