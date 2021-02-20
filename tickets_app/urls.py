from django.urls import path
from . import views as ticket_views 
from .views import TicketsListView

urlpatterns = [
    path("order/create/", ticket_views.order_create, name="order-create"),
    path("profile", ticket_views.profile, name="profile"),
    path("", TicketsListView.as_view(), name="home"),
    path("orders", ticket_views.orders, name="orders"),
]