from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('events/', views.event_listing, name='events'),
    path('events/detail/<int:pk>', views.event_detail, name='detail'),
    path('events/my_events/', views.my_events, name='my_events'),
    path('create_event/', views.create_event, name='create_event'),
]
