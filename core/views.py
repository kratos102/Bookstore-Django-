from book.models import *
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from django.views.generic import DetailView
from .forms import CreateUSerForm
from django.contrib import auth, messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.mixins import LoginRequiredMixin
from order.models import Order

def shop(request):
    category = request.GET.get('category')
    if category == None:
        items = Book.objects.all()
    else:
        items = Book.objects.filter(category__name = category)
    categories = Category.objects.all()
    context = {
        'items': items,
        'categories': categories,
        }
    return render(request, 'homepage/shop.html', context)

class ProductDetailView(DetailView):
    model = Book
    template_name = "homepage/product.html"

class Home(View):
    def get (self, request):
        return render(request, 'homepage/index.html')

def registerPage(request):
    if request.user.is_authenticated:
        return redirect('index')
    else:
        form = CreateUSerForm()
        if request.method == 'POST':
            form = CreateUSerForm(request.POST)
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get('username')
                messages.success(request, 'Account was created for ' + user)
                return redirect('login')
        context = {'form': form}
        return render(request, 'homepage/register.html', context)

def loginPage(request):
    if request.user.is_authenticated:
        return redirect('index')
    else:
        if request.method == 'POST':
            username= request.POST.get('username')
            password= request.POST.get('password')

            user = authenticate(request, username= username, password= password)

            if user is not None:
                login(request,user)
                return redirect('index')
            else:
                messages.info(request, 'Username OR Password is incorrect')
        context = {}
        return render(request, 'homepage/login.html', context)

def logoutUser(request):
    logout(request)
    return redirect('index')

class OrderSummaryView(LoginRequiredMixin, View):
    login_url = '/login/'
    redirect_field_name = 'login'
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            context = {
                'object': order
            }
            return render(self.request, 'homepage/cart.html', context)
        except ObjectDoesNotExist:
            messages.warning(self.request, "You do not have an active order")
            return redirect("/")

from django.views.decorators.http import require_GET

@require_GET
def searchView(request):
    if 'search'in request.GET:
        context = request.GET['search']
        items = Book.objects.filter(title__icontains=context)
    else:
        items = Book.objects.none()
    return render(request, 'homepage/search.html', {'items': items})
