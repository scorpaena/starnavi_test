from django.urls import path
from .views import (
    Register,
    Login,
    logout_view,
    UserLastLogin
)

urlpatterns = [
    path('register/', Register.as_view(), name='register'),
    path('login/', Login.as_view(), name='login'),
    path('logout/', logout_view, name='logout'),
    path('last_login/', UserLastLogin.as_view(), name='last_login')
]
