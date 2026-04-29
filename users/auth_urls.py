from django.urls import path
from .auth_views import ms_login, ms_callback, ms_logout

urlpatterns = [
    path('login/', ms_login, name='ms-login'),
    path('callback/', ms_callback, name='ms-callback'),
    path('logout/', ms_logout, name='ms-logout'),
]
