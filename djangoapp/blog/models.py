from django.contrib.auth.models import User
from django.db import models
from utils.rands import new_slug
from utils.resize_image import resize_img


# Create your models here.
class Tag(models.Model):
    class Meta:
        verbose_name = 'Tag'
        verbose_name_plural = 'Tag'

    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, default=None, null=True,
                            blank=True, max_length=255)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = new_slug(self.name, k=5)
        return super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.name


class Category(models.Model):
    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, default=None, null=True,
                            blank=True, max_length=255)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = new_slug(self.name, k=5)
        return super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.name


class Page(models.Model):
    class Meta:
        verbose_name = 'Page'
        verbose_name_plural = 'Pages'

    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, default=None, null=True,
                            blank=True, max_length=255)

    is_published = models.BooleanField(default=False)
    content = models.TextField()

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = new_slug(self.title, k=5)
        return super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.title


class Post(models.Model):
    class Meta:
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'

    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, default='', null=True,
                            blank=True, max_length=255)

    excerpt = models.CharField(max_length=155)
    is_published = models.BooleanField(default=False)
    content = models.TextField()
    cover = models.ImageField(upload_to='posts/%Y/%m',
                              blank=True, default=None)
    cover_in_post_content = models.BooleanField(default=True)

    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL,
        blank=True, null=True, default=None)
    tags = models.ManyToManyField(Tag, blank=True, default=None)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    created_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, related_name='post_created_by',
        blank=True, null=True)
    updated_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, related_name='post_updated_by',
        blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = new_slug(self.title, k=5)

        current_cover_name = str(self.cover.name)
        super_save = super().save(*args, **kwargs)
        cover_changed = False

        if self.cover:
            cover_changed = current_cover_name != self.cover.name

        if cover_changed:
            resize_img(self.cover, 900, otimize=True, quality=75)

        return super_save

    def __str__(self) -> str:
        return self.title
