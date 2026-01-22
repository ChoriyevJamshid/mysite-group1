from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from blog.models import Post
from blog.choices import PostStatus


def post_list(request):
    posts = Post.published.all()

    paginator = Paginator(posts, 5)
    page_number = request.GET.get('page', 1)

    try:
        posts = paginator.page(page_number)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    except PageNotAnInteger:
        posts = paginator.page(1)

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
