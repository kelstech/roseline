from django.urls import include, path
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register("devices", views.DeviceViewSet, basename="auth-devices")

urlpatterns = [
    path("auth/login", views.login, name="auth-login"),
    path("auth/refresh", views.refresh, name="auth-refresh"),
    path("auth/logout", views.logout, name="auth-logout"),
    path("auth/health", views.health, name="auth-health"),
    path("auth/", include(router.urls)),
]
