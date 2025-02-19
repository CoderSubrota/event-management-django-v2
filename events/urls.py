from django.urls import path
from events.views import (
  AddEventView,CreateParticipantView,CreateCategoryView,
  OrganizerDashboardView,CategoryListView,CategoryUpdateView,
  CategoryDeleteView,EventListView,EventUpdateView,
  ParticipantListView,ParticipantUpdateView , ParticipantDeleteView,
  RSVPEventView,EventDetailView,RSVPsView,ContactUsView
)

urlpatterns =[
    path("add_event/", AddEventView.as_view(), name='add_event') ,
    path("add_participant/", CreateParticipantView.as_view(), name='add_participant'),
    path("create_category/", CreateCategoryView.as_view(), name='create_category'),
    path("dashboard/", OrganizerDashboardView.as_view(), name='dashboard'),
    # Event URLs
    path('events/', EventListView.as_view(), name='event_list'),
    path('events/edit/<int:pk>/',EventUpdateView.as_view(), name='event_update'),
    path('events/delete/<int:pk>/',EventUpdateView.as_view(), name='event_delete'),

    # Participant URLs
    path('participants/',ParticipantListView.as_view(), name='participant_list'),
    path('participants/edit/<int:pk>/',ParticipantUpdateView.as_view(), name='participant_update'),
    path('participants/delete/<int:pk>/',ParticipantDeleteView.as_view(), name='participant_delete'),

    # Category URLs
    path('categories/',CategoryListView.as_view(), name='category_list'),
    path('categories/edit/<int:pk>/',CategoryUpdateView.as_view(), name='category_update'),
    path('categories/delete/<int:pk>/',CategoryDeleteView.as_view(), name='category_delete'),
  #rsvp 
   path('event/<int:event_id>/rsvp/', RSVPEventView.as_view(), name='rsvp_event'),
   path('event/<int:event_id>/', EventDetailView.as_view(), name='event_detail'),
   path('event_dashboard', RSVPsView.as_view(), name='event_rsvps_dashboard'),
  #----------------
  path('contact_us',ContactUsView.as_view(),name='contact_us')
]
