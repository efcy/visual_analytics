from django.urls import path
from .views import *

urlpatterns = [
    path('authenticated', CheckAuthenticatedView.as_view(), name='authenticated'),
    path('register', SignupView.as_view(), name='register'),
    path('login', LoginView.as_view(), name='login'),
    path('logout', LogoutView.as_view(), name='logout'),
    path('delete', DeleteAccountView.as_view(), name='delete_account'),
    path('csrf_cookie', GetCSRFToken.as_view(), name='csrf_cookie'),
    path('user', GetUserProfileView.as_view(), name='user_profile'),
    path('update', UpdateUserProfileView.as_view(), name='update_profile'),
]