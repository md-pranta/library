from django.urls import path
from .views import UserRegistation,Userlogin,userlogout,profileview,Details,deposit,Borrowed_Book,Comment_views,returnBook

urlpatterns = [
    path('register/',  UserRegistation.as_view(), name='register'),
    path('login/',  Userlogin.as_view(), name='login'),
    path('logout/', userlogout.as_view(), name='logout'),
    path('profile/',profileview, name='profile'),
    path('details/<int:pk>/', Details.as_view(), name='details'),
    path('deposit/', deposit, name='deposit'),
    path("borrow/<int:id>", Borrowed_Book, name="borrow_book"),
    path('comments/<int:pk>/', Comment_views.as_view(), name='comment_views'),
    path('return/<int:id>', returnBook, name='return'),
]
