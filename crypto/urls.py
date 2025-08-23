from django.urls import path
from rest_framework.routers import DefaultRouter

from crypto import views

router = DefaultRouter()
router.register(r'coins', views.CoinViewSet)

urlpatterns = []

urlpatterns += router.urls
