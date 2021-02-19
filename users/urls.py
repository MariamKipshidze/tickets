from django.contrib.auth import views as auth_views
from . import views as user_views

urlpatterns = [
    path("login/", auth_views.LoginView.as_view(template_name="users/login.html"), name="login"),
    path('register/', user_views.user_register, name="register"),
]