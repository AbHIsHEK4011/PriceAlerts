from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AlertViewSet,RegistrationView

router = DefaultRouter()
router.register(r'alerts', AlertViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('register/', RegistrationView.as_view(), name='register'),

]
