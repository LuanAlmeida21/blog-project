from blog.models import Post
from django.core.paginator import Paginator
from django.shortcuts import render

COUNT_PAGE = 9


def index(request):
    posts = Post.objects.get_is_published()
    paginator = Paginator(posts, COUNT_PAGE)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        'blog/pages/index.html',
        {
            'page_obj': page_obj,
        }
    )


def created_by(request, author_pk):
    posts = Post.objects.get_is_published().filter(created_by__pk=author_pk)
    paginator = Paginator(posts, COUNT_PAGE)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        'blog/pages/index.html',
        {
            'page_obj': page_obj,
        }
    )


def category(request, category_pk):
    posts = Post.objects.get_is_published().filter(category__pk=category_pk)
    paginator = Paginator(posts, COUNT_PAGE)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        'blog/pages/index.html',
        {
            'page_obj': page_obj,
        }
    )


def page(request):

    return render(
        request,
        'blog/pages/page.html',
        {
            # 'page_obj': page_obj,
        }
    )


def post(request, slug):
    post = Post.objects.get_is_published().filter(slug=slug).first()

    return render(
        request,
        'blog/pages/post.html',
        {
            'post': post
        }
    )
