from django.http import Http404
from django.shortcuts import render, get_object_or_404

from blog.models import Post
from blog.choices import PostStatus


def post_list(request):
    posts = Post.published.all()
    return render(request,
                  'blog/post/list.html',
                  {'posts': posts})


def post_detail(request, year: int, month: int, day: int, slug: str):

    post = get_object_or_404(Post,
                             slug=slug,
                             publish__year=year,
                             publish__month=month,
                             publish__day=day,
                             status=PostStatus.PUBLISHED)

    return render(request,
                  "blog/post/detail.html",
                  {"post": post})
