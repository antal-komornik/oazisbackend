from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import UserProfileForm

# Create your views here.


def profile(requset):
    return render(requset, 'profile.html')
