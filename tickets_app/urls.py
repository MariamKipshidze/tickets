from django.urls import path
from . import views as ticket_views 
from .views import TicketsListView, TicketDetailview, OrderDetailView

urlpatterns = [
    path("order/create/", ticket_views.order_create, name="order-create"),
    path("profile", ticket_views.profile, name="profile"),
    path("", TicketsListView.as_view(), name="home"),
    path("ticket/<int:pk>/detail/", TicketDetailview.as_view(), name="ticket-detail"),
    path("order/<int:pk>/detail/", OrderDetailView.as_view(), name="order-detail"),
    path("orders/", ticket_views.orders, name="orders"),
]