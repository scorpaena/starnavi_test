from django.urls import path
from datetime import datetime
from . import views
from .dateconverter import YearMonthDayConverter


urlpatterns = [
    path('', views.PostList.as_view(), name = 'post_list'),
    path('<int:post_id>/', 
        views.PostDetail.as_view(), name = 'post_detail'
    ),
    path('<yyyy-mm-dd:from>/<yyyy-mm-dd:to>', 
        views.LikesInDatesRange.as_view(), name = 'postsindatesrange_list'
    ),
]
