from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('images/', views.images, name='images'),
    path('search_images/', views.search_images, name='search_images'),
    path('galleries/', views.galleries, name='galleries'),
    path('search_galleries/', views.search_galleries, name='search_galleries'),
    path('setlastimg/<int:pk>/<int:page_nr>', views.SetLastViewedImg, name='setlastimg'),
    path('setlastgal/<int:pk>/<int:page_nr>', views.SetLastViewedGal, name='setlastgal'),
]