from django.shortcuts import render
from users.models import User
from .models import Ticket, Order
from .forms import TicketsSearchForm, OrderCreateForm

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.core.handlers.wsgi import WSGIRequest
from django.contrib import messages
from django.urls import reverse

import datetime
from django.utils import timezone
from django.db.models import Q, Sum

@login_required
def orders(request: WSGIRequest) -> HttpResponse:
    user = request.user
    orders = Order.objects.filter(user=user)

    return render(request, "tickets_app/orders.html", context={
        "orders": orders,
    })


@login_required
def profile(request: WSGIRequest) -> HttpResponse:
    user = request.user
    tickets = Ticket.objects.filter(tk_order__user=user)
    tickets_search_form = TicketsSearchForm()
    orders_info = {}

    if request.method == "GET":
        tickets_search_form = TicketsSearchForm(request.GET)
        if tickets_search_form.is_valid():
            data = tickets_search_form.cleaned_data["order_search"]
            if data == "1":
                orders_info = Ticket.objects.aggregate(spent_money=Sum("price", filter=Q(tk_order__user=user)))
                tickets = Ticket.objects.filter(Q(start_date__gte=(timezone.now()\
                - datetime.timedelta(weeks=1))),Q(tk_order__user=user)).order_by("-start_date")
            elif data == "2":
                orders_info = Ticket.objects.aggregate(spent_money=Sum("price", filter=Q(tk_order__user=user)))
                tickets = Ticket.objects.filter(Q(start_date__gte=(timezone.now()\
                 - datetime.timedelta(days=30))),Q(tk_order__user=user)).order_by("-start_date")
            elif data == "3":
                orders_info = Ticket.objects.aggregate(spent_money=Sum("price", filter=Q(tk_order__user=user)))
                tickets = Ticket.objects.filter(Q(start_date__gte=(timezone.now()\
                 - datetime.timedelta(days=365))), Q(tk_order__user=user)).order_by("-start_date")

    return render(request, 'tickets_app/profile.html', context={
        "user": user,
        "tickets": tickets,
        "tickets_search_form": tickets_search_form,
        "orders_info": orders_info
    })


@login_required
def order_create(request: WSGIRequest) -> HttpResponse:
    user = request.user
    order_form = OrderCreateForm()

    if request.method == "POST":
        order_form = OrderCreateForm(request.POST)
        if order_form.is_valid():
            order = order_form.save(commit=False)
            order.user = user
            order.save

            messages.success(request, f"Successfully booked")
            return HttpResponseRedirect(reverse("profile"))

    return render(request, "tickets_app/order_form.html", context={
        "order_form": order_form,
        })
