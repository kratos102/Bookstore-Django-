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
from order.models import *
from .forms import CheckoutForm, PaymentMethodForm
from django.http import HttpResponseRedirect, request

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


def is_valid_form(values):
    valid = True
    for field in values:
        if field == '':
            valid = False
    return valid

class CheckoutView(View):
    def get(self, request, *args, **kwargs):
        saved_address = Address.objects.get_or_create(user = request.user)
        saved_address = saved_address[0]
        form = CheckoutForm()
        payment_method = PaymentMethodForm()
        order_qs = Order.objects.filter(user = request.user, ordered = False)
        order_item = order_qs[0].items.all()
        order_total = order_qs[0].get_total()

        context = {
            'adress': form,
            'order_item': order_item,
            'order_total': order_total,
            'payment_method': payment_method
        }
        return render (request,'homepage/checkout.html', context)
    def post(self, request, *args, **kwargs):
        saved_adress = Address.objects.get_or_create(user = request.user)
        saved_adress = saved_adress[0]
        form = CheckoutForm(instance=saved_adress)
        payment_obj = Order.objects.filter(user = request.user, ordered = False)[0]
        payment_form = PaymentMethodForm(instance= payment_obj)
        if request.method == 'post' or request.method == 'POST':
            form = CheckoutForm(request.POST, instance=saved_adress)
            pay_form = PaymentMethodForm(request.POST, instance= payment_obj)
            if form.is_valid() and pay_form.is_valid:
                form.save()
                pay_method = pay_form.save()
                
                if pay_method.payment_method == 'Cash on Delivery':
                    order_qs = Order.objects.filter(user= request.user, ordered = False)
                    order = order_qs[0]
                    order.ordered = True
                    order.orderId = order.id
                    order.paymentId = pay_method.payment_method 
                    order.save()
                    order_items = OrderItem.objects.filter(user = request.user, ordered = False)
                    for item in order_items:
                        item.ordered = True
                        item.save()
                    messages.info(request,'Order Submited Succesfully, Thank you!')
                    return redirect('index')
                
                if pay_method.payment_method == 'Paypal':
                    messages.info(request,'This payment method not supported yet, please choose another payment')
                    return redirect('checkout')