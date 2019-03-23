from django.urls import path

from . import views

app_name = 'events'

urlpatterns = [
	path('all/', views.event_listing, name='events'),
	path('create/', views.create_event, name='create_event'),
	path('mine/', views.my_events, name='my_events'),

	path('events/detail/<slug:slug>/', views.event_detail, name='detail'),
	path('events/update/<slug:slug>/', views.update_event, name='update_event'),
	path('events/delete/<slug:slug>/', views.delete_event, name='delete_event'),

	path('<int:event_id>/create_run/', views.create_event_run,
		 name='create_event_run'),
	path('update_run/<int:event_run_id>/', views.update_event_run,
		 name='update_event_run'),
	path('delete_run/<int:event_run_id>/', views.delete_event_run,
		 name='delete_event_run'),

	path('<category>/', views.event_listing, name='events_by_category'),
]
