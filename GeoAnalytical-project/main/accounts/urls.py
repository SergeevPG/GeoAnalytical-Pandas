from django.urls import path 
from . import views
urlpatterns = [
    # Описание параметров метода path
    #   1) - адрессная строка 
    #   2) - метод в views 
    #   3) - название ссылки для использования в href html
    path('register', views.register, name="register"),
    path('login', views.login, name="login"),
    path('logout', views.logout, name="logout"),
    # path('success_registration', views.success_registration, name="success_registration"),
]