from django.urls import path
from . import views as ticket_views 

urlpatterns = [
    path("order/create/", ticket_views.order_create, name="order-create"),
    path("", ticket_views.profile, name="profile"),
]