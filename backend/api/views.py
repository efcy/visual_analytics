from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from rest_framework import generics,viewsets
from . import serializers
from rest_framework.permissions import IsAuthenticated, AllowAny
from . import models

from django.http import JsonResponse
from django.views.decorators.http import require_GET

from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action

@require_GET
def health_check(request):
    return JsonResponse({"message": "UP"}, status=200)

class FrameTimeViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.FrameTimeSerializer
    permission_classes = [IsAuthenticated]
    queryset = models.FrameTime.objects.all()

    def list(self, request, *args, **kwargs):
        # Keep the original list behavior
        return super().list(request, *args, **kwargs)

    #overloading the create function to allow lists and single objects as input
    def create(self, request, *args, **kwargs):
        data = request.data
        if isinstance(data, list):
            serializer = self.get_serializer(data=data, many=True)
        else:
            serializer = self.get_serializer(data=data)
        
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


    def destroy(self, request, *args, **kwargs):
        # Override destroy method to handle both single and bulk delete
        if kwargs.get('pk') == 'all':
            deleted_count, _ = self.get_queryset().delete()
            return Response({'message': f'Deleted {deleted_count} objects'}, status=status.HTTP_204_NO_CONTENT)
        return super().destroy(request, *args, **kwargs)

class SensorLogViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.SensorLogSerializer
    permission_classes = [IsAuthenticated]
    queryset = models.SensorLog.objects.all()

    def list(self, request, *args, **kwargs):
        # Keep the original list behavior
        return super().list(request, *args, **kwargs)

    #overloading the create function to allow lists and single objects as input
    def create(self, request, *args, **kwargs):
        data = request.data
        print(data)
        if isinstance(data, list):
            serializer = self.get_serializer(data=data, many=True)
        else:
            serializer = self.get_serializer(data=data)
        
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        print(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


    def destroy(self, request, *args, **kwargs):
        # Override destroy method to handle both single and bulk delete
        if kwargs.get('pk') == 'all':
            deleted_count, _ = self.get_queryset().delete()
            return Response({'message': f'Deleted {deleted_count} objects'}, status=status.HTTP_204_NO_CONTENT)
        return super().destroy(request, *args, **kwargs)

class CreateUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer
    permission_classes = [AllowAny]

class EventViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.EventSerializer
    permission_classes = [IsAuthenticated]
    queryset = models.Event.objects.all()

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        id = self.request.query_params.get("id")
        name = self.request.query_params.get("name")

        if id is not None:
            # If id is provided, return a single object
            event = get_object_or_404(queryset, id=id)
            serializer = self.get_serializer(event)
            return Response(serializer.data)
        elif name is not None:
            queryset = queryset.filter(name__icontains=name)
        
        # For other cases, proceed with normal list behavior
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def get_queryset(self):
        return models.Event.objects.all()


class GameViewSet(viewsets.ModelViewSet):
    queryset = models.Game.objects.all()
    serializer_class = serializers.GameSerializer
    permission_classes = [IsAuthenticated]
    """this approach to get games related to events is not really good 
        see serializers.py for an better example"""    
    def get_queryset(self):
        event_id = self.request.query_params.get("event")
        if event_id is not None:
            return models.Game.objects.filter(event=event_id)
        else:
            return models.Game.objects.all()
        
class RobotDataViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = models.RobotData.objects.all()
    serializer_class = serializers.RobotDataSerializer

    def get_queryset(self):
        game_id = self.request.query_params.get("game")
        if game_id is not None:
            return models.Log.objects.filter(game=game_id)
        else:
            return models.Log.objects.all()

class ImageViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = models.Image.objects.all()
    serializer_class = serializers.ImageSerializer

    def get_queryset(self):
        log_id = self.request.query_params.get("log")
        print("log_id", log_id)
        if log_id is not None:
            return models.Image.objects.filter(log=log_id)
        else:
            return models.Image.objects.all()

class CameraMatrixViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = models.CameraMatrix.objects.all()
    serializer_class = serializers.CameraMatrixSerializer

class ImageAnnotationViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = models.ImageAnnotation.objects.all()
    serializer_class = serializers.ImageAnnotationSerializer