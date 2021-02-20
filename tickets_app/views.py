from django.shortcuts import render
from users.models import User
from .models import Ticket, Order
from .forms import TicketsSearchForm, OrderCreateForm

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.urls import reverse

import datetime
from django.utils import timezone


@login_required
def profile(request):
    user = request.user
    orders = user.order.all()
    tickets_search_form = TicketsSearchForm()
    #order_info = {}

    if request.method == "GET":
        tickets_search_form = TicketsSearchForm(request.GET)
        if tickets_search_form.is_valid():
            data = tickets_search_form.cleaned_data["order_search"]
            if data == "1":
                # order_info = user.order.filter(end_date__lte=timezone.now()) \
                #     .aggregate(
                #     spent_money=Sum(
                #         'order',
                #         filter=Q(start_date__gte=(timezone.now() - datetime.timedelta(weeks=1))))
                #     ),
                orders = user.orders.filter(start_date__gte=(timezone.now()\
                - datetime.timedelta(weeks=1))).order_by("-start_date")
            elif data == "2":
                orders = user.orders.filter(start_date__gte=(timezone.now()\
                 - datetime.timedelta(days=30))).order_by("-start_date")
            elif data == "3":
                orders = user.orders.filter(start_date__gte=(timezone.now()\
                 - datetime.timedelta(days=365))).order_by("-start_date")

    return render(request, 'tickets_app/profile.html', context={
        "user": user,
        "orders": orders,
        "tickets_search_form": tickets_search_form,
        # **order_info
    })


@login_required
def order_create(request):
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
