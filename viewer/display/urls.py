from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('images/', views.images, name='images'),
    path('galleries/', views.galleries, name='galleries'),
    path('setlastimg/<int:pk>/<int:page_nr>', views.SetLastViewedImg, name='setlastimg'),
    path('setlastgal/<int:pk>', views.SetLastViewedGal, name='setlastgal'),
]