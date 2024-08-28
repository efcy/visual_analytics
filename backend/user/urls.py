from django.urls import path
from rest_framework.authtoken import views
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
    path('api-token-auth/', views.obtain_auth_token),
    path('token',GetUserToken.as_view(),name='get_token')
]