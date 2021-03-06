from django.shortcuts import render
from users.models import User
from .models import Ticket, Order
from .forms import TicketsSearchForm, OrderCreateForm, OrderForm

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.core.handlers.wsgi import WSGIRequest
from django.contrib import messages
from django.urls import reverse

import datetime
from django.utils import timezone
from django.db.models import Q, Sum
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.views.generic import ListView, DetailView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin


class UsersListView(ListView):
    model = User
    template_name = "tickets_app/users_list.html"
    context_object_name = "users"

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            users = User.objects.filter(email__icontains=query)
        else:
            users = User.objects.all()
        return users


class TicketsListView(ListView):
    model = Ticket
    template_name = "tickets_app/home.html"
    context_object_name = "tickets"
    paginate_by = 5


class TicketDetailview(DetailView):
    model = Ticket

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['order_form'] = OrderForm()
        return context

    @staticmethod
    def post(request, *args, **kwargs):
        order_form = OrderForm(request.POST)
        if order_form.is_valid():
            order = order_form.save(commit=False)
            order.user = request.user
            order.ticket_id = kwargs["pk"]
            if order.user.balance - order.ticket.price > 0:
                order.user.balance = order.user.balance - order.ticket.price
                order.save()
                order.user.save()
                messages.success(request, f"Successfully completed")
            else:
                messages.warning(request, f"There is not enough money on your balance")

        return redirect(to='ticket-detail', **kwargs)


class OrderDetailView(LoginRequiredMixin, DetailView):
    model = Order


class OrderDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Order
    success_url = "/orders/"

    def test_func(self):
        order = self.get_object()
        if self.request.user == order.user:
            return True
        return False

    def post(self, request, *args, **kwargs):
        order = self.get_object()
        order.user.balance = order.user.balance + order.ticket.price
        order.user.save()
        messages.success(request, f"Successfully deleted")

        return self.delete(request, *args, **kwargs)


@login_required
def orders(request: WSGIRequest) -> HttpResponse:
    user = request.user
    orders = Order.objects.filter(user=user)

    q = request.GET.get('q')

    if q:
        orders = Order.objects.filter(Q(ticket__name__icontains=q), Q(user=user))

    page = request.GET.get('page', 1)
    paginator = Paginator(orders, 5)
    try:
        orders = paginator.page(page)
    except PageNotAnInteger:
        orders = paginator.page(1)
    except EmptyPage:
        orders = paginator.page(paginator.num_pages)

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
                orders_info = Ticket.objects.aggregate(spent_money=Sum("price",
                filter=Q(tk_order__user=user,\
                        start_date__gte=(timezone.now()- datetime.timedelta(weeks=1)))))
                tickets = Ticket.objects.filter(Q(start_date__gte=(timezone.now()\
                - datetime.timedelta(weeks=1))),Q(tk_order__user=user)).order_by("-start_date")
            elif data == "2":
                orders_info = Ticket.objects.aggregate(spent_money=Sum("price",
                filter=Q(tk_order__user=user,\
                         start_date__gte=(timezone.now()- datetime.timedelta(days=30)))))
                tickets = Ticket.objects.filter(Q(start_date__gte=(timezone.now()\
                 - datetime.timedelta(days=30))),Q(tk_order__user=user)).order_by("-start_date")
            elif data == "3":
                orders_info = Ticket.objects.aggregate(spent_money=Sum("price",
                filter=Q(tk_order__user=user,\
                         start_date__gte=(timezone.now()- datetime.timedelta(days=365)))))
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

            if user.balance - order.ticket.price > 0:
                user.balance = user.balance - order.ticket.price
                user.save()
                order.save()
                messages.success(request, f"Successfully completed")
            else:
                messages.warning(request, f"There is not enough money on your balance")

            return HttpResponseRedirect(reverse("profile"))

    return render(request, "tickets_app/order_form.html", context={
        "order_form": order_form,
        })
