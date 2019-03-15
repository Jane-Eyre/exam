# coding=utf-8
# from django.conf.urls import url
from django.urls import path
# from django.contrib import admin

from . import views

urlpatterns = [
    path('show/', views.show),
    path('answer/', views.answer),
    path('summary/', views.summary),
    path('single/', views.single),
    path('summary_detail/', views.summary_detail),
    # url(r'^show/', views.test),
    # url(r'^answer/', views.answer),
    # url(r'^summary', views.summary),

]
