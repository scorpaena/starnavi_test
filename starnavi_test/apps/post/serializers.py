from rest_framework import serializers
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from datetime import datetime
from .models import Post, UserLikes


class CurrentUserDefault:
    '''
    overridden to get .user.id in lieu of .user 
    since ForeignKeyField in model is utilized
    '''
    requires_context = True
    def set_context(self, serializer_field):
        self.user_id = serializer_field.context.get('request').user.id

    def __call__(self, serializer_field):
        return serializer_field.context.get('request').user.id

    def __repr__(self):
        return unicode_to_repr('%s()' % self.__class__.__name__)


class PostSerializer(serializers.ModelSerializer):
    user_id = serializers.HiddenField(default=CurrentUserDefault())
    user = serializers.CharField(source='user.username', read_only=True)
    class Meta:
        model = Post
        fields = [
            'id',
            'title', 
            'content',
            'date_posted', 
            'likes',
            'user_id',
            'user'
        ]
        read_only_fields = ['likes']


class PostDetailSuperSerializer(serializers.ModelSerializer):
    user_id = serializers.HiddenField(default=CurrentUserDefault())
    user = serializers.CharField(source='user.username', read_only=True)
    class Meta:
        model = Post
        fields = [
            'id',
            'title', 
            'content', 
            'date_posted', 
            'likes',
            'user_id',
            'user'
        ]
        read_only_fields = ['user', 'date_posted']

    def update(self, instance, validated_data, owner_or_admin=True):
        post = instance.id
        likes = validated_data.get('likes')
        user = validated_data.get('user_id') #currently logged in user
        if owner_or_admin: #if False, this fields are ommitted (applies for PostDetailGenegalSerializer)
            title = validated_data.get('title')
            content = validated_data.get('content')
        else:
            pass
        try:
            user_exists = UserLikes.objects.get(user=user, post=post)
        except ObjectDoesNotExist:
            UserLikes.objects.create(
                user=User.objects.get(id=user), 
                post=Post.objects.get(id=post), 
                like_dislike=likes
            )
        else:
            post_author = Post.objects.get(id=post).user #original author of the post
            instance.likes = likes
            instance.user = post_author #otherwise, instance.user = currently logged in user
            if owner_or_admin: #if False, this fields are left 'as-is' (applies for PostDetailGenegalSerializer)
                instance.title = title
                instance.content = content
            else:
                pass
            UserLikes.objects.filter(post=post, user=user).update(
                date_liked=datetime.today(), 
                like_dislike=likes
            )
        instance.save()
        return instance


class PostDetailGenegalSerializer(PostDetailSuperSerializer): #to keep DRY
    class Meta(PostDetailSuperSerializer.Meta):
        read_only_fields = ['user', 'date_posted','content','title']

    def update(self, instance, validated_data):
        return super().update(instance, validated_data, owner_or_admin=False)

#no need so far, since user = serializers.CharField is defined in superClass
    # def to_representation(self, instance): 
        # rep = super().to_representation(instance)
        # rep['user'] = instance.user.username
        # return rep

class UserLikesSerializer(serializers.ModelSerializer):
    likes_count = serializers.IntegerField(source='total', read_only=True)
    
    class Meta:
        model = UserLikes
        fields = [
            'id',
            'date_liked', 
            'like_dislike',
            'likes_count'
        ]
