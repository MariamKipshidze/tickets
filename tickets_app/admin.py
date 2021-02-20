from django.contrib import admin
from .models import Order, Ticket

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ["user", "ticket"]


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display =["barcode", "name","price"]