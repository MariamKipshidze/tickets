from django.contrib import admin
from .models import Order, Ticket

@admin.register(Order)
class Useradmin(UserAdmin):
    list_display = ["ticket", "user"]


@admin.register(Ticket)
class Useradmin(UserAdmin):
    list_display =["name"]