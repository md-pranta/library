from django.contrib import admin
from .models import BookModel,CategoryModel
# Register your models here.
class CatAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug' : ('name', )}
    list_display = ['name', 'slug']
    
admin.site.register(CategoryModel, CatAdmin)
admin.site.register(BookModel)