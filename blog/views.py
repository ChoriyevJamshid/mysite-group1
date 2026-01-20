from django.http import Http404
from django.shortcuts import render, get_object_or_404

from blog.models import Post
from blog.choices import PostStatus


def post_list(request):
    posts = Post.published.all()
    return render(request,
                  'blog/post/list.html',
                  {'posts': posts})


def post_detail(request, pk):
    # try:
    #     post = Post.published.get(pk=pk)
    # except Post.DoesNotExist:
    #     raise Http404("Post does not exist")

    post = get_object_or_404(Post,
                             pk=pk,
                             status=PostStatus.PUBLISHED)

    return render(request,
                  "blog/post/detail.html",
                  {"post": post})
