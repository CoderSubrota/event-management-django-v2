from django.urls import path
from events.views import add_event_form,create_participant_view,create_category,organizer_dashboard,participant_delete
from events.views import create_category,category_list,category_update,category_delete,event_list,event_update,event_delete,participant_list,participant_update

urlpatterns =[
    path("add_event/", add_event_form, name='add_event') ,
    path("add_participant/", create_participant_view, name='add_participant'),
    path("create_category/", create_category, name='create_category'),
    path("dashboard/", organizer_dashboard, name='dashboard'),
    # Event URLs
    path('events/', event_list, name='event_list'),
    path('events/add/',add_event_form, name='event_create'),
    path('events/edit/<int:pk>/',event_update, name='event_update'),
    path('events/delete/<int:pk>/',event_delete, name='event_delete'),

    # Participant URLs
    path('participants/',participant_list, name='participant_list'),
    path('participants/add/',create_participant_view, name='participant_create'),
    path('participants/edit/<int:pk>/',participant_update, name='participant_update'),
    path('participants/delete/<int:pk>/',participant_delete, name='participant_delete'),

    # Category URLs
    path('categories/',category_list, name='category_list'),
    path('categories/add/',create_category, name='category_create'),
    path('categories/edit/<int:pk>/',category_update, name='category_update'),
    path('categories/delete/<int:pk>/',category_delete, name='category_delete'),
]
