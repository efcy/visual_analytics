from django.urls import path
from . import views
from rest_framework import routers

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

app_name = 'api'

urlpatterns = [
    path('',views.scalar_doc,name="scalar_doc"),
    path('health/',views.health_check,name="health_check"),
    path('image-count/', views.ImageCountView.as_view(), name='image-count'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('behavior/filter/', views.BehaviorFrameOptionAPIView.as_view(), name='behavior-filter'),
    path('behavior/count/', views.BehaviorFrameCountView.as_view(), name='behavior-count'),
    path('behavior/symbol/count/', views.BehaviorSymbolCountView.as_view(), name='behavior-count'),
    path('cognitionrepr/count/', views.CognitionReprCountView.as_view(), name='cognitionrepr-count'),
    path('motionrepr/count/', views.MotionReprCountView.as_view(), name='motionnrepr-count'),
    path('image/update/', views.ImageUpdateView.as_view(), name='image-update'),
]

router = routers.DefaultRouter()
router.register('events',views.EventViewSet)
router.register('games', views.GameViewSet)
router.register('experiments', views.ExperimentViewSet)
router.register('logs',views.LogViewSet)
router.register('image',views.ImageViewSet)
router.register('annotations',views.AnnotationViewSet)
router.register("cognitionrepr",views.CognitionRepresentationViewSet)
router.register("motionrepr",views.MotionRepresentationViewSet)
router.register("behavior-option",views.BehaviorOptionViewSet)
router.register("behavior-option-state",views.BehaviorOptionStateViewSet)
router.register("behavior-frame-option",views.BehaviorFrameOptionViewSet)
router.register("behavior/symbol/complete",views.XabslSymbolCompleteViewSet)
router.register("behavior/symbol/sparse",views.XabslSymbolSparseViewSet)
router.register("log-status",views.LogStatusViewSet)
router.register("frame-filter",views.FrameFilterView)

urlpatterns += router.urls
