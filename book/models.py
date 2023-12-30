from django.db import models
from django.contrib.auth.models import User


class CategoryModel(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True, null=True, blank=True)

    def __str__(self):
        return self.name


class BookModel(models.Model):
    category = models.ManyToManyField(CategoryModel)
    image = models.ImageField(upload_to='uploads/', blank=True, null=True)
    title = models.CharField(max_length=100)
    description = models.TextField()
    price = models.CharField(max_length=15)
    
    def __str__(self):
        return self.title