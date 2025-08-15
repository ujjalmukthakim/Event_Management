from .views import sign_in,sign_up,activate_user
from django.urls import path

urlpatterns = [
    path('',sign_in,name="sign-in"),
    path('signup/',sign_up,name="sign-up"),
    path('activate/<int:user_id>/<str:token>/',activate_user, name='activate-user')
]