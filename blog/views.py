from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.mail import send_mail
from django.conf import settings

from django.views.generic import ListView

from blog.models import Post, Comment
from blog.choices import PostStatus
from blog.forms import EmailPostForm, CommentForm


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

    comments = post.comments.filter(active=True)
    form = CommentForm()

    context = {
        "post": post,
        "form": form,
        "comments": comments,
    }

    return render(request,
                  "blog/post/detail.html",
                  context=context)


def post_share(request, post_id: int):
    post = get_object_or_404(Post,
                             id=post_id,
                             status=PostStatus.PUBLISHED)

    sent = False

    if request.method == 'POST':
        print(f"\n{request.POST}\n")
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            print(f"\n{cd = }\n")

            post_url = request.build_absolute_uri(
                post.get_absolute_url())

            subject = f"{cd['name']} recommends you read {post.title}"

            message = (f"Read {post.title} at {post_url}\n\n"
                       f"{cd['name']}'s comments: {cd['comments']}")

            send_mail(
                subject=subject,
                message=message,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[cd['to']]
            )
            sent = True

    else:
        form = EmailPostForm()

    return render(request,
                  'blog/post/share.html',
                  {
                      'form': form,
                      'post': post,
                      'sent': sent
                  })


@require_POST
def post_comment(request, post_id: int):
    post = get_object_or_404(Post,
                             id=post_id,
                             status=PostStatus.PUBLISHED)
    comment = None

    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.save()

    context = {"post": post,
               "form": form,
               "comment": comment}

    return render(request,
                  'blog/comment.html',
                  context=context)


class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = "posts"
    paginate_by = 3
    template_name = 'blog/post/list.html'
