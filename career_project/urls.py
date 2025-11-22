# from django.urls import path, include
# urlpatterns=[path('', include('careerapp.urls'))]

from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    path("", include("careerapp.urls")),
    path("", RedirectView.as_view(url="/")),
]

