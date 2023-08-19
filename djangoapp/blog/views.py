from typing import Any

from blog.models import Page, Post
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db.models import Q
from django.db.models.query import QuerySet
from django.http import Http404, HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.views.generic import ListView

COUNT_PAGE = 9


class PostListView(ListView):
    model = Post
    context_object_name = 'posts'
    template_name = 'blog/pages/index.html'
    ordering = ['-pk']
    paginate_by = COUNT_PAGE
    queryset = Post.objects.get_is_published()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'site_title': 'Home'
        }
        )
        return context


class CreatedByListView(PostListView):
    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self._temp_context = {}

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        user = self._temp_context['user']

        user_full_name = user.username
        if user.first_name:
            user_full_name = f'{user.first_name} {user.last_name}'

        ctx.update({
            'site_title': 'Post de ' + user_full_name,
        })

        return ctx

    def get(self, request, *args, **kwargs):
        author_pk = self.kwargs.get('author_pk')
        user = User.objects.filter(pk=author_pk).first()

        if user is None:
            return redirect('blog:index')

        self._temp_context = {
            'author_pk': author_pk,
            'user': user,
        }
        return super().get(request, *args, **kwargs)

    def get_queryset(self) -> QuerySet[Any]:
        qs = super().get_queryset()
        qs = qs.filter(created_by__pk=self._temp_context['user'].pk)
        return qs


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
