from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('events/', views.event_listing, name='events'),
    path('events/detail/<int:pk>/', views.event_detail, name='detail'),
    path('events/mine/', views.my_events, name='my_events'),
    path('events/create/', views.create_event, name='create_event'),
    path('events/delete/<int:pk>/', views.delete_event, name='delete_event'),
	path('events/update/<int:pk>/', views.update_event, name='update_event'),
]
