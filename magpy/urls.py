from django.contrib import admin
from django.urls import include, path, re_path
from rest_framework import routers

from api import views

router = routers.SimpleRouter()
router.register(r'projects', views.ProjectViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
]
