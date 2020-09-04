import django_filters
from django.db.models import Q
from .models import Post

class PostFilter(django_filters.FilterSet):
    
    def user_contains(self, qs, contains, value):
        lookup = Q(user__id__icontains=value)|\
            Q(user__username__icontains=value)
        return qs.filter(lookup)

    def date_contains(self, qs, contains, value):
        lookup = Q(date_posted__icontains=value)
        return qs.filter(lookup)

    def title_contains(self, qs, contains, value):
        lookup = Q(title__icontains=value)
        return qs.filter(lookup)

    def content_contains(self, qs, contains, value):
        lookup = Q(content__icontains=value)
        return qs.filter(lookup)
    
    user = django_filters.filters.CharFilter(method = 'user_contains')
    date_posted = django_filters.filters.CharFilter(method = 'date_contains')
    title = django_filters.filters.CharFilter(method = 'title_contains')
    content = django_filters.filters.CharFilter(method = 'content_contains')
    id = django_filters.NumberFilter()

    class Meta:
        model = Post
        fields = [
            'id',
            'title', 
            'content',
            'date_posted',
            'user'
        ]
