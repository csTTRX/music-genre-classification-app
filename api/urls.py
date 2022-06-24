from django.urls import path, include, re_path
from .views import upload_viewset
from rest_framework import routers

router = routers.SimpleRouter()
router.register(r'', upload_viewset, basename="upload")

# urlpatterns = [
#     path('', upload_viewset, name = 'upload')
# ]

urlpatterns = [
    path('', include(router.urls)),
]