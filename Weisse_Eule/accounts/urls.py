from django.urls import path,include
from . import views

app_name = "accounts"

urlpatterns = [
    path('login/', views.login_user, name="login"),
    path('create_user/', views.create_user, name="create_user"),
    path('logout/', views.logout_user, name="logout"),
]