from blog import views
from django.urls import path

app_name = 'blog'

urlpatterns = [
    path('', views.index, name='index'),
    path('post/<slug:slug>/', views.post, name='post'),
    path('created_by/<int:author_pk>/', views.created_by, name='created_by'),
    path('category/<int:category_pk>/', views.category, name='category'),
    path('page/', views.page, name='page'),
]
