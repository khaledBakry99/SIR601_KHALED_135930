# BIA601 - Dr.Bassel Alkhatib
# samar_115286
# mhd_hussam_109817

from django.urls import path
from . import views


# Adding the url of the application as '' (The one and only page)
urlpatterns = [
    path('', views.main_page_view, name='main_page_view'),
    path('main/', views.main_page_view, name='main_page_view'),
    path('not-found/', views.not_found_page_view, name='not_found_page_view'),
    path('search/<int:identifier>/', views.search_page_view, name='search_page_view'),
]
