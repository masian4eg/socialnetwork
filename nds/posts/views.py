from django.shortcuts import render
from .models import Post
# from django.views.generic import ListView


# class PostList(ListView):
    # model = Post
    # template_name = 'posts/main.html'
    # context_object_name = 'posts'
    # qs = Post.objects.all()
    #
    # def post_comment_create_and_list_view(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     return context


def post_comment_create_and_list_view(request):
    qs = Post.objects.all()

    context = {
        'qs': qs,
    }

    return render(request, 'posts/main.html', context)
