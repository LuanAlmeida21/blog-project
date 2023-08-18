from blog.models import Page, Post
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import Http404
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
            'site_title': 'Home',
        }
    )


def created_by(request, author_pk):
    user = User.objects.filter(pk=author_pk).first()

    if user is None:
        raise Http404()

    user_full_name = user.username
    if user.first_name:
        user_full_name = f'{user.first_name} {user.last_name}'

    posts = Post.objects.get_is_published().filter(created_by__pk=author_pk)
    paginator = Paginator(posts, COUNT_PAGE)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        'blog/pages/index.html',
        {
            'page_obj': page_obj,
            'site_title': 'Posts de ' + user_full_name,
        }
    )


def category(request, slug):
    posts = Post.objects.get_is_published().filter(category__slug=slug)
    paginator = Paginator(posts, COUNT_PAGE)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    if len(page_obj) == 0:
        raise Http404

    site_title = f'{page_obj[0].category.name} - Categoria'

    return render(
        request,
        'blog/pages/index.html',
        {
            'page_obj': page_obj,
            'site_title': site_title,
        }
    )


def tags(request, slug):
    posts = Post.objects.get_is_published().filter(tags__slug=slug)
    paginator = Paginator(posts, COUNT_PAGE)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    if len(page_obj) == 0:
        raise Http404

    site_title = f'{page_obj[0].tags.first().name} - Tags'

    return render(
        request,
        'blog/pages/index.html',
        {
            'page_obj': page_obj,
            'site_title': site_title,
        }
    )


def page(request, slug):

    page_obj = Page.objects.filter(is_published=True, slug=slug).first()

    if page_obj is None:
        raise Http404

    site_title = f'{page_obj.title} - Página'

    return render(
        request,
        'blog/pages/page.html',
        {
            'page': page_obj,
            'site_title': site_title,
        }
    )


def post(request, slug):
    post_obj = Post.objects.get_is_published().filter(slug=slug).first()

    if post_obj is None:
        raise Http404

    site_title = f'{post_obj.title} - Post'

    return render(
        request,
        'blog/pages/post.html',
        {
            'post': post_obj,
            'site_title': site_title,
        }
    )


def search(request):
    search_value = request.GET.get('search', '').strip()
    posts = Post.objects.get_is_published().filter(
        Q(title__icontains=search_value) |
        Q(content__icontains=search_value) |
        Q(excerpt__icontains=search_value)
    )[:COUNT_PAGE]

    site_title = f'{search_value[:30]} - Search'

    return render(
        request,
        'blog/pages/index.html',
        {
            'page_obj': posts,
            'search_value': search_value,
            'site_title': site_title,
        }
    )
