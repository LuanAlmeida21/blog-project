from django.db import models
from utils.rands import new_slug


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
