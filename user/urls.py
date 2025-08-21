from .views import sign_in,sign_up,activate_user,user_profile,edit_profile,change_password
from django.urls import path

urlpatterns = [
    path('',sign_in,name="sign-in"),
    path('signup/',sign_up,name="sign-up"),
    path('activate/<int:user_id>/<str:token>/',activate_user, name='activate-user'),
    path('profile/', user_profile, name='user-profile'),
    path('profile/edit/', edit_profile, name='edit-profile'),
    path('profile/change-password/', change_password, name='change-password'),
]