from django.contrib import admin
from .models import UserAccountModel,BorrowedModel,Comment
# Register your models here.
admin.site.register(UserAccountModel)
admin.site.register(BorrowedModel)
admin.site.register(Comment)