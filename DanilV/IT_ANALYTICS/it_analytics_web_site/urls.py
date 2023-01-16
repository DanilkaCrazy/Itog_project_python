from . import views

from django.urls import path
 

urlpatterns = [
    path('', views.index),
    path('demand', views.demand),
    path('cities', views.cities),
    path('top_10_skills', views.top_10_skills),
    path('api_headhunter_vacancies', views.api_headhunter_vacancies),
]