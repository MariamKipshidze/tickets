from django import forms
from .models import Order

class TicketsSearchForm(forms.Form):
    CHOICE = (("1", "last week"), ("2", "last month"), ("3", "last year"))
    order_search = forms.ChoiceField(choices=CHOICE, required=False)


class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ["ticket"]