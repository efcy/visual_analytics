from django.urls import path
from . import views
from rest_framework import routers
from drf_spectacular.views import SpectacularSwaggerView,SpectacularAPIView


urlpatterns = [
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('schema/swagger-ui/',SpectacularSwaggerView.as_view(url_name='schema'),name='swagger-ui'),
    path('health/',views.health_check,name="health_check"),
    path('api/frametime/all/', views.FrameTimeViewSet.as_view({'delete': 'destroy'}))
]

router = routers.DefaultRouter()
router.register('events',views.EventViewSet)
router.register('games', views.GameViewSet)
router.register('logs',views.LogViewSet)
router.register('image',views.ImageViewSet)
router.register('imageannotation',views.ImageAnnotationViewSet)
router.register('camera_matrix',views.CameraMatrixViewSet)
router.register("frametime",views.FrameTimeViewSet)

urlpatterns += router.urls