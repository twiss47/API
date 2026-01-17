from django.contrib import admin
from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token
from app.views import LogoutView   
urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/token/", obtain_auth_token),
    path("api/logout/", LogoutView.as_view()),  
    path("app/", include("app.urls")),
]
