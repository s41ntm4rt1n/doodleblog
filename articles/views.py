from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

def index(request):
    messages.error(request, "Email already exists. Please use a different email.")
    return render(request, 'index.html')
