from .views import home,see_and_change_roles,show_group,create_group,update_group,delete_group,delete_event,all_events,edit_event,create_event,create_category,rsvp_event,dashboard,delete_participant,sign_out
from django.urls import path
from django.conf import settings
from django.views.generic import TemplateView

from django.conf.urls.static import static



urlpatterns = [ 
    path('home/',home,name="home"),
    path('group/',show_group,name='group_related_work'),
    path('role/',see_and_change_roles,name='see-and-change-roles'),
     path('create_group/', create_group, name='create_group'),
     path('groups/<int:group_id>/update/', update_group, name='update_group'),
    path('groups/<int:group_id>/delete/', delete_group, name='delete_group'),
    path('events/',all_events,name='all_events'),
    path('event/edit/<int:id>/', edit_event, name='edit_event'),
    path('create_event',create_event,name='create_event'),
    path('create_category',create_category,name='create_category'),
    path('event/delete/<int:id>/', delete_event, name='delete_event'),
    path('event/<int:event_id>/rsvp/', rsvp_event, name='rsvp_event'),
    path('no-permission/', TemplateView.as_view(template_name="no_permission.html"), name='no-permission'),
    path('participant/<int:user_id>/delete/', delete_participant, name='delete_participant'),path('logout/', sign_out, name='sign-out'),



    path('dashboard/', dashboard, name='dashboard'),
    path('show_group/',show_group)
    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)