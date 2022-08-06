from django.urls import path
from . import views
from django.views.decorators.cache import cache_page


app_name='post'

urlpatterns = [
    path('', views.index, name='index'),
    path('post/<int:pk>/',(cache_page(300))(views.detail), name='detail'),
    path('login/', views.logining, name='login'),
    path('register', views.register, name='register'),
    path('total/', views.visit_post_information, name='total'),
    path('score/', views.system_score_information, name='score'),
    path('order/', views.order, name='order'),
    path('order/delete/<int:pk>/', views.order_delete, name='delete'),
    path('orders_delete/', views.orders_delete, name='orders_delete'),
    path('order/update/', views.order_update, name='order_update'),
]