
from django.contrib import admin
from django.urls import path, include
from application import views
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token


root = DefaultRouter()
root.register(r'product', views.ProductViewset, basename='product')
root.register(r'order', views.OrderViewset, basename='order')
root.register(r'orderitem', views.OrderItemViewset, basename='orderitem')




urlpatterns = [
    path('', include(root.urls)),
    path('admin/', admin.site.urls),   
    path('login/', obtain_auth_token, name='api-auth-token'),
]
