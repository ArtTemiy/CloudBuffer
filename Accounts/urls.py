from django.urls import path
from .views import RegisterView, LogInView, LogOutView, login_done, register_done, \
    profile_view, logout_done

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('register-done/', register_done, name='register-done'),
    path('login/', LogInView.as_view(), name='login'),
    path('login-done/', login_done, name='login-done'),
    path('logout/', LogOutView.as_view(), name='logout'),
    path('logout-done/', logout_done, name='logout-done'),
    path('profile/', profile_view, name='profile')
]
