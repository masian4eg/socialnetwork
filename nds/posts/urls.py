from django.urls import path
from .views import like_unlike_post, PostDeleteView, PostUpdateView, post_comment_create_and_list_view

app_name = 'posts'

urlpatterns = [
    path('', post_comment_create_and_list_view, name='main-post-view'), # http://127.0.0.1:8000/posts
    path('liked/', like_unlike_post, name='like-post-view'),
    path('<pk>/delete', PostDeleteView.as_view(), name='post-delete'),
    path('<pk>/update', PostUpdateView.as_view(), name='post-update'),
]

# path('', PostList.as_view())