from .models import User
from django.contrib.auth.forms import UserCreationForm


class UserCreation(UserCreationForm):
    class Meta:
        model = User
        fields = ["email", "first_name", "last_name", "mobile_number"]