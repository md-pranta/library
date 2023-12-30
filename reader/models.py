from django.db import models
from django.contrib.auth.models import User
from book.models import BookModel

# Create your models here.
class UserAccountModel(models.Model):
    user = models.OneToOneField(User, related_name='account', on_delete=models.CASCADE)
    account_no = models.IntegerField(unique=True)
    balance = models.DecimalField(default=0, max_length=6, max_digits=10000, decimal_places=2)
    
    def __str__(self):
        return str(self.account_no)
    
class BorrowedModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(BookModel, on_delete=models.CASCADE)
    borrowed_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return {self.user.username}

class Comment(models.Model):
    book = models.ForeignKey(BookModel, on_delete = models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete = models.CASCADE, related_name='user')

    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add = True)
    