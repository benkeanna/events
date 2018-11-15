from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('events/', views.event_listing, name='events'),
    path('eventruns/', views.eventrun_listing, name='eventruns'),
    path('events/<name>', views.event_detail, name='detail'),
]
