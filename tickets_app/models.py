from django.db import models
from django.utils.translation import gettext_lazy as _
from users.models import User


class Ticket(models.Model):
    name = models.CharField(max_length=100, verbose_name=_("Name"))
    price = models.DecimalField(max_digits=4, decimal_places=2, verbose_name=_('Price'))
    start_date = models.DateTimeField(verbose_name=_("Start Date"))
    end_date = models.DateTimeField(verbose_name=_("End date"))
    barcode = models.PositiveSmallIntegerField(verbose_name=_("Barcode"), unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Ticket')
        verbose_name_plural = _('tickets')


class Order(models.Model):
    user = models.ForeignKey(User, verbose_name=_("User"), on_delete=models.CASCADE, related_name="order")
    ticket = models.OneToOneField(Ticket, verbose_name=("Ticket"), on_delete=models.CASCADE, related_name="tk_order")

    def __str__(self):
        return self.user.email

    class Meta:
        verbose_name = _('Order')
        verbose_name_plural = _('Orders')