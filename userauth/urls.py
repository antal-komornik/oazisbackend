from django.urls import path, include
from dashboard.views import profile
from .views import UserProfileListView


urlpatterns = [
    path('', include('allauth.urls')),
    # path('profile/', profile, name='profile'),
    path('profiles/users/', UserProfileListView.as_view(), name='user-list'),


]
