from django import forms 
from .models import CategoryModel, BookModel

class CategoryForm(forms.ModelForm):
    class Meta:
        model = CategoryModel
        fields = '__all__'
        
class BookForm(forms.ModelForm):
    class Meta:
        model = BookModel
        fields = '__all__'
        