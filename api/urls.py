from django.urls import path, include, re_path
from .views import upload_viewset
from rest_framework import routers
from django.views.generic import TemplateView

router = routers.SimpleRouter()
router.register(r'', upload_viewset, basename="upload")

# urlpatterns = [
#     path('', upload_viewset, name = 'upload')
# ]

urlpatterns = [
    path('', include(router.urls)),
    re_path(r'^.*', TemplateView.as_view(template_name='index.html')),
]