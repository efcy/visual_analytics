from django.contrib.auth.models import User
from rest_framework import generics,viewsets
from . import serializers
from rest_framework.permissions import IsAuthenticated, AllowAny
from . import models

class CreateUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer
    permission_classes = [AllowAny]

class EventViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.EventSerializer
    permission_classes = [IsAuthenticated]
    queryset = models.Event.objects.all()

    def get_queryset(self):
        """
        this is for the event search bar, maybe I can do this better/faster and with less database querying
        However this should never be that slow since we wont have that many events anyway
        """
        qs = models.Event.objects.all()
        name = self.request.query_params.get("name")
        id = self.request.query_params.get("id")

        if name is not None:
            qs = qs.filter(name__icontains=name)
        if id is not None:
            qs = qs.filter(id=id).first()
        return qs


class GameViewSet(viewsets.ModelViewSet):
    queryset = models.Game.objects.all()
    serializer_class = serializers.GameSerializer
    """this approach to get games related to events is not really good 
        see serializers.py for an better example"""    
    def get_queryset(self):
        event_id = self.request.query_params.get("event")
        if event_id is not None:
            return models.Game.objects.filter(event=event_id)
        else:
            return models.Game.objects.all()
        
class LogViewSet(viewsets.ModelViewSet):
    queryset = models.Log.objects.all()
    serializer_class = serializers.LogSerializer

class ImageViewSet(viewsets.ModelViewSet):
    queryset = models.Image.objects.all()
    serializer_class = serializers.ImageSerializer

class CameraMatrixViewSet(viewsets.ModelViewSet):
    queryset = models.CameraMatrix.objects.all()
    serializer_class = serializers.CameraMatrixSerializer

class ImageAnnotationViewSet(viewsets.ModelViewSet):
    queryset = models.ImageAnnotation.objects.all()
    serializer_class = serializers.ImageAnnotationSerializer