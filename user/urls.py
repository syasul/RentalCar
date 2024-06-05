from django.urls import path

from . import views

urlpatterns = [
    path('login-admin/', views.loginAdmin, name="loginAdmin"),
    path('login-user/', views.loginUser, name="loginUser"),
    path('register-user/', views.registerUser, name="registerUser"),
    path('logout/', views.logout, name="logout")
]