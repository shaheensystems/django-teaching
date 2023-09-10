from django.contrib.auth.views import LoginView, LogoutView
from .views import register_view  
from django.urls import path
urlpatterns = [
    path('signin/', LoginView.as_view(template_name='signin.html'), name='signin'),
    path('register/', register_view, name='register'),
    path('signout/', LogoutView.as_view(next_page='/'), name='signout'),
]
