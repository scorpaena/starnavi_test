from django.shortcuts import get_object_or_404
from django.db.models import Count
# from django.db.models.query import QuerySet
from django.contrib.auth.models import User
from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django.utils.timezone import datetime
from django.contrib.sessions.models import Session
from .models import Post, UserLikes
from .filters import PostFilter
from .serializers import (
    PostSerializer, 
    PostDetailGenegalSerializer, 
    PostDetailSuperSerializer,
    UserLikesSerializer
)


class PostList(generics.ListCreateAPIView):
    queryset = Post.objects.all().order_by('-date_posted')
    serializer_class = PostSerializer
    filterset_class = PostFilter
    permission_classes = [IsAuthenticatedOrReadOnly]


class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    def get_serializer_class(self):
        obj = get_object_or_404(Post, pk=self.kwargs.get('post_id'))
        if self.request.user == obj.user or self.request.user.is_staff:
            return PostDetailSuperSerializer
        return PostDetailGenegalSerializer

    def get_object(self):
        obj = get_object_or_404(Post, pk=self.kwargs.get('post_id'))
        return obj


class LikesInDatesRange(generics.ListAPIView):
    serializer_class = UserLikesSerializer

    def get_queryset(self):
        # query = UserLikes.objects.all().query
        # query.group_by = ['date_liked']
        # post_user = QuerySet(query=query, model=UserLikes)

        date_from = self.kwargs.get('from')
        date_to = self.kwargs.get('to')
        
        post_user = UserLikes.objects.values('date_liked').filter(
            date_liked__gte = date_from, 
            date_liked__lte = date_to
            ).annotate(total = Count('like_dislike'))
        return post_user
