from django.shortcuts import render,redirect,get_object_or_404

# Create your views here.
from book.models import BookModel,CategoryModel
from .models import BorrowedModel
from django.views.generic import FormView, DetailView, CreateView
from .forms import RegisterForm
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, LogoutView
from django.views import View
from .forms import DepositForm, CommentForm

from django.views.generic import TemplateView
# Create your views here.
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib import messages
from . import models

# for email
from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.template.loader import render_to_string

def returnBook(request, id):
    record = BorrowedModel.objects.get(pk=id)
    request.user.account.balance += int(record.book.price)
    request.user.account.save()
    record.delete()
    messages.success(
        request,
        f' Borrowsuccessfully Return the book'
        )

    sendTransactionEmail(request.user, int(record.book.price), "return book message", "return_email.html")
    return redirect('profile')


def sendTransactionEmail(user,amount,subject,template):
    message= render_to_string(template,{
            'user':user,
            'amount':amount
        })
    send_mail = EmailMultiAlternatives(subject, '',to=[user.email])
    send_mail.attach_alternative(message,'text/html')
    send_mail.send()

class UserRegistation(FormView):
    template_name = 'signup.html'
    form_class = RegisterForm
    success_url =reverse_lazy('home')
    
    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return super().form_valid(form)

class Userlogin(LoginView):
    template_name = 'signin.html'
    def get_success_url(self):
        return reverse_lazy('home')
    
class userlogout(View):
    def get(self, request):
        logout(request)
        return redirect('home')
    
def deposit(request):
    form = DepositForm()
    user = request.user.account  
    if request.method == 'POST':
        form = DepositForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            user.balance += amount
            user.save()
            messages.success(
            request,
            f'{"{:,.2f}".format(float(amount))}$ was deposited to your account successfully'
            )

            sendTransactionEmail(request.user, amount, "Deposit Message", "deposit_mail.html")
            return redirect('home')
    return render(request, 'deposit.html', {'form': form})


def profileview(request):
    data = BorrowedModel.objects.filter(user=request.user)
    return render(request, 'profile.html', {'data':data})


class Details(DetailView):
    model = BookModel
    template_name = 'details.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        book = self.get_object()
        comments = book.comments.all()
        comment_form = CommentForm()
        context['comments'] = comments
        context['comment_form'] = comment_form
        context['book'] = book
        return context

def Borrowed_Book(request, id):
    book = get_object_or_404(BookModel, pk=id)
    balance = int(request.user.account.balance)
    price = int(book.price)

    if balance >= price:
        BorrowedModel.objects.create(user=request.user, book=book)
        request.user.account.balance -= price
        request.user.account.save()

        messages.success(
            request,
            f'{"{:,.2f}".format(float(price))}$ was Borrowed Book successfully'
            )

        sendTransactionEmail(request.user, price, "Borrowed Book Message", "borrowed_mail.html")
    else:
        messages.success(
            request,
            f'you don`t have enough money! '
            )
    return redirect(reverse("details", args=[book.id]))


class Comment_views(DetailView):
    model = BookModel
    template_name = 'comment.html'
 
    def post(self, request, *args, **kwargs):
        comment_form = CommentForm(data=self.request.POST)
        book = self.get_object()
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.book = book
            new_comment.user = request.user
          
            
            new_comment.save()
        return self.get(request, *args, **kwargs)
 
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        book = self.object
        comments = book.comments.all()
        comment_form = CommentForm()
        context['comments'] = comments
        context['comment_form'] = comment_form
        context['book'] = book
        return context
