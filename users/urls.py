from django.urls import path
from users.views import sign_up,sign_in,sign_out,send_email,activate_account,admin_dashboard,assign_role,manage_users,create_group,group_list,view_events,add_participant,show_event_list
urlpatterns = [
     path("sign-up/", sign_up,name="sign-up") ,
     path("sing-in/", sign_in,name="sign-in") ,
     path("sing-out/", sign_out,name="sign-out") ,
     path("send-mail/", send_email,name="send-mail") ,
     path("admin/manage-users/", manage_users, name="manage_users"),
     path("activate/<int:user_id>/<str:token>/", activate_account),
     path("admin/dashboard", admin_dashboard,name='admin_dashboard'),
     path("admin/<int:user_id>/assign-role", assign_role,name="assign-role"),
     path("admin/create-group", create_group,name="create-group"),
     path("admin/group-list", group_list,name="group-list"),
     path("organizer/view-events", view_events,name="view-events"),
     path("add-participant", add_participant,name="add-participant"),
     path("show_event_list", show_event_list,name="show_event_list"),
     
]