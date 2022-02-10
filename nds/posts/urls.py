from django.urls import path
from .views import post_comment_create_and_list_view

app_name = 'posts'

urlpatterns = [
    path('', post_comment_create_and_list_view, name='main-post-view'), # http://127.0.0.1:8000/posts
]

# path('', PostList.as_view())