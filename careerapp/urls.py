# from django.urls import path
# from . import views
# urlpatterns=[
#  path('', views.index),
# ]


from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("api/skill-gap/", views.api_skill_gap, name="api_skill_gap"),
    path("api/roadmap/", views.api_roadmap, name="api_roadmap"),
    path("api/news/", views.api_news, name="api_news"),
]
