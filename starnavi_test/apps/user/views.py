from django.http import HttpResponse
from rest_framework import generics
from rest_framework.response import Response
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .serializers import (
    UserSerializer, 
    AuthenticationSerializer, 
    UserLastLoginSerializer
)


class Register(generics.CreateAPIView):
    serializer_class = UserSerializer


class Login(generics.CreateAPIView):
    serializer_class = AuthenticationSerializer

    def post(self, request):
        data = request.data
        username = data['username']
        password = data['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                data = {'success': 'Sucessfully logged in'}
            else:
                data = {'error': 'Your account has been disabled'}
        else:
            data = {'error': 'Error: check username/password'}
        return Response(data)

def logout_view(request):
    logout(request)
    data = 'You are logged out'
    return HttpResponse(data)


class UserLastLogin(generics.ListAPIView):
    queryset = User.objects.all().order_by('-last_login')
    serializer_class = UserLastLoginSerializer
