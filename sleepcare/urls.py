from django.contrib import admin
from django.urls import path, include
from monitoreo.views import ultimas_alertas

urlpatterns = [
    path("admin/", admin.site.urls),

    # API principal
    path("api/", include("monitoreo.urls")),

    # 🔥 endpoint directo de alertas (opcional pero útil)
    path("api/ultimas_alertas/", ultimas_alertas),
]