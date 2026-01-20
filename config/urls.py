from django.contrib import admin
from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token
from app.views import LogoutView   
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/token/",TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/logout/", LogoutView.as_view()),
    path('api/token/refresh/', TokenRefreshView.as_view()),   
    path("", include("app.urls")),
]
