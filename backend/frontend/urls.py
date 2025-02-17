from django.urls import path
from django.views.generic import RedirectView
from . import views

urlpatterns = [
    path('', RedirectView.as_view(url='/events')),
    path('login', views.LoginView, name='mylogin'),
    path('logout', views.LogoutView, name='mylogout'),
    path('signup', views.SignupView, name='signup'),
    path('events', views.EventListView.as_view(), name='events'),
    path('events/<int:pk>', views.GameListView.as_view(), name='event_detail'),
    path('games/<int:pk>', views.LogListView.as_view(), name='game_detail'),
    path('log/<int:pk>', views.ImageListView.as_view(), name='log_detail'),
    path('log/<int:pk>/frame/<int:bla>', views.ImageDetailView.as_view(), name='image_detail'),
    path('games/<int:pk>/multiview/frame/<int:frame>', views.MultiView.as_view(), name='multiview_detail'),
]