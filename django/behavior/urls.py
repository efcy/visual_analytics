from django.urls import path
from . import views
from rest_framework import routers

app_name = "behavior"

urlpatterns = [
    path(
        "behavior/filter/",
        views.BehaviorFrameOptionAPIView.as_view(),
        name="behavior-filter",
    ),
    path(
        "behavior/count/", views.BehaviorFrameCountView.as_view(), name="behavior-count"
    ),
    path(
        "behavior/symbol/count/",
        views.BehaviorSymbolCountView.as_view(),
        name="behavior-count",
    ),
]

router = routers.DefaultRouter()
router.register("behavior-option", views.BehaviorOptionViewSet)
router.register("behavior-option-state", views.BehaviorOptionStateViewSet)
router.register("behavior-frame-option", views.BehaviorFrameOptionViewSet)
router.register("behavior/symbol/complete", views.XabslSymbolCompleteViewSet)
router.register("behavior/symbol/sparse", views.XabslSymbolSparseViewSet)

urlpatterns += router.urls
