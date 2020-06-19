from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<str:pk>', views.UnleashedSalesOrderView.as_view(), name='salesorder-detail'),
]
