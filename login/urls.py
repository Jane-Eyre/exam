# coding=utf-8
from django.urls import path
from . import views

urlpatterns = [
    path('show/', views.show),
    path('answer/', views.answer),
    path('summary/', views.summary),
    path('single/', views.single),
    path('summary_detail/', views.summary_detail),
    path('problems/', views.problems),
    # url(r'^show/', views.test),
    # url(r'^answer/', views.answer),
    # url(r'^summary', views.summary),

]
