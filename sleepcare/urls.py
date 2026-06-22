from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),

    # API principal (Ya incluye por defecto el endpoint de ultimas_alertas)
    path("api/", include("monitoreo.urls")),
]