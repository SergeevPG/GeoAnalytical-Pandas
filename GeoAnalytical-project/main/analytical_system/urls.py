from django.urls import path 
from . import views
urlpatterns = [
    # Описание параметров метода path
    #   1) - адрессная строка 
    #   2) - метод в views 
    #   3) - название ссылки для base.html
    path('', views.index, name='home'),
    path('analysis-module', views.analysis_module, name='analysis_module'),
    # path('test', views.test_html, name='test_html'),
]