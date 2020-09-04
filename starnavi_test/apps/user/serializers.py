from rest_framework import serializers
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate


class UserSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(max_length=128, 
        write_only=True, style={'input_type': 'password'}
    )
    password2 = serializers.CharField(max_length=128, 
        write_only=True, style={'input_type': 'password'}
    )

    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'email',
            'first_name',
            'last_name',
            'last_login',
            'is_staff',
            'is_superuser',
            'password1',
            'password2',
        ]
        read_only_fields = ['id', 'is_staff', 'is_superuser', 'last_login']

    def create(self, validated_data):
        password1 = validated_data.pop('password1', '')
        password2 = validated_data.pop('password2', '')

        if password1 and password2 and password1 != password2:
            raise ValidationError('password mismatch')

        user = User.objects.create(**validated_data)
        user.set_password(password1)
        user.save()
        return user


class AuthenticationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=128, 
        write_only=True, style={'input_type': 'password'}
    )

    class Meta:
        model = User
        fields = [
            'username',
            'password',
        ]
    
    def create(self, validated_data):
        if self.is_valid():
            username = self.validated_data['username']
            password = self.validated_data['password']
            if not authenticate(username=username, password=password):
                return ValidationError('username or password are incorrect')


class UserLastLoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'email',
            'first_name',
            'last_name',
            'last_login',
            'is_staff',
            'is_superuser',
        ]
