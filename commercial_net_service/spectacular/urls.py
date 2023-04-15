from django.urls import path

from drf_spectacular.views import SpectacularSwaggerView

urlpatterns = [
    path('doc',
         SpectacularSwaggerView.as_view(url_name='schema'),
         name='swagger-ui'),
]
