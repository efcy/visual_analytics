from django.urls import path
from . import views
from rest_framework import routers

app_name = 'motion'

urlpatterns = [
    path('motionframe/count/', views.MotionFrameCount.as_view(), name='motionframe-count'),
]

router = routers.DefaultRouter()
router.register("motionframe",views.MotionFrameViewSet)

urlpatterns += router.urls