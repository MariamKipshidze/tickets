from django.shortcuts import render
from .forms import UserCreation


def user_register(request):
    user_form = UserCreation()
    if request.method == "POST":
        user_form = UserCreation(request.POST)
        if user_form.is_valid():
            user_form.save()
            messages.success(request, f"Account created successfully!")
            return redirect("login")

    return render(request, "tickets_app/register.html", context={
        "user_form": user_form
        })
