from django.shortcuts import render
from reader.models import BookModel
from book.models import CategoryModel
# Create your views here.

def home(req,category_slug=None):
    data = BookModel.objects.all()
    if category_slug is not None:
        category = CategoryModel.objects.get(slug = category_slug)
        data = BookModel.objects.filter(category = category)
        
    categories = CategoryModel.objects.all()
    return render(req, 'home.html', {'data':data, 'category': categories})


