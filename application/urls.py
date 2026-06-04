from django.urls import path, include
from .views import ProductViewset, OrderViewset, OrderItemViewset
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token


root = DefaultRouter()
root.register(r'product', ProductViewset, basename='product')
root.register(r'order', OrderViewset, basename='order')
root.register(r'orderitem', OrderItemViewset, basename='orderitem')






urlpatterns = [
    
    path('api/', include(root.urls)),
    path('login/', obtain_auth_token, name='api-auth-token'),
]

