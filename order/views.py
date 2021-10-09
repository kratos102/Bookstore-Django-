
from django.contrib.auth import forms
from django.contrib.auth.decorators import login_required
from django.http import request
from django.utils import timezone
from django.views.generic.base import View
from book.models import Book
from django.shortcuts import get_object_or_404, redirect, render
from .models import Order, OrderItem
from django.contrib import messages



@login_required(login_url='login')
def add_to_shoppingcart(request, slug):
    item = get_object_or_404(Book, slug = slug)
    order_item, created = OrderItem.objects.get_or_create(  
        item = item,
        user = request.user,
        ordered = False
    )
    order_qs = Order.objects.filter(user= request.user, ordered = False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__slug= item.slug).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(request, "this item quantity updated")
            return redirect("order-summary")
        else:
            messages.info(request, "this item was added to your cart") 
            order.items.add(order_item)
            order_item.save()
            return redirect("order-summary")
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(user= request.user, ordered_date = ordered_date)
        order.items.add(order_item)
        messages.info(request, "this item was added to your cart")
        return redirect("order-summary")

@login_required(login_url='login')
def remove_from_cart(request, slug):
    item = get_object_or_404(Book, slug = slug)
    order_qs = Order.objects.filter(user= request.user, ordered = False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__slug= item.slug).exists():
            order_item=OrderItem.objects.filter(  
                item = item,
                user = request.user,
                ordered = False
            )[0]
            order.items.remove(order_item)
            order_item.quantity = 1
            order_item.save()
            messages.info(request, "this item was remove from your cart")
            return redirect("order-summary")
        else:
            messages.info(request, "this item was not in your cart")
            return redirect("product",slug= slug)

    else:
        messages.info(request, "you do not have an active order")
        return redirect("product",slug= slug)

@login_required(login_url='login')
def remove_single_item_from_cart(request, slug):
    item = get_object_or_404(Book, slug=slug)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
            else:
                order.items.remove(order_item)
                order_item.save()
            messages.info(request, "This item quantity was updated.")
            return redirect("order-summary")
        else:
            messages.info(request, "This item was not in your cart")
            return redirect("product", slug=slug)
    else:
        messages.info(request, "You do not have an active order")
        return redirect("product", slug=slug)

