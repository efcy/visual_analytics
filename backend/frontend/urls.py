from django.urls import path
from . import views

urlpatterns = [
    path('', views.LoginView, name='login'),
    path('signup', views.SignupView, name='signup'),
    path('events', views.EventListView.as_view(), name='events'),
    path('events/<int:pk>', views.GameListView.as_view(), name='event_detail'),
    path('games/<int:pk>', views.LogListView.as_view(), name='game_detail'),
    path('log/<int:pk>', views.ImageListView.as_view(), name='log_detail'),
    path('log/<int:pk>/frame/<int:bla>', views.ImageDetailView.as_view(), name='image_detail'),
    path('process-canvas-data/', views.process_canvas_data, name='process_canvas_data'),
    
]