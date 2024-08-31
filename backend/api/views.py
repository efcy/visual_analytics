
from django.shortcuts import get_object_or_404
from rest_framework import generics,viewsets
from . import serializers
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from . import models
from django.http import JsonResponse
from django.views.decorators.http import require_GET
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import Q

User = get_user_model()

@require_GET
def health_check(request):
    return JsonResponse({"message": "UP"}, status=200)


class SensorLogViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.SensorLogSerializer
    #permission_classes = [IsAuthenticated]
    queryset = models.SensorLog.objects.all()

    def list(self, request, *args, **kwargs):
        # Keep the original list behavior
        return super().list(request, *args, **kwargs)

    #overloading the create function to allow lists and single objects as input
    def create(self, request, *args, **kwargs):
        data = request.data
        print("request.data:", data)
        if isinstance(data, list):
            serializer = self.get_serializer(data=data, many=True)
        else:
            serializer = self.get_serializer(data=data)
        print("serializer created")
        

        serializer.is_valid(raise_exception=False)
        print(serializer.errors)
        print("serializer.is_valid")
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
    permission_classes = [AllowAny]
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
    permission_classes = [AllowAny]
    """this approach to get games related to events is not really good 
        see serializers.py for an better example"""    
    def get_queryset(self):
        event_id = self.request.query_params.get("event")
        if event_id is not None:
            return models.Game.objects.filter(event=event_id)
        else:
            return models.Game.objects.all()
        
class RobotDataViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    queryset = models.RobotData.objects.all()
    serializer_class = serializers.RobotDataSerializer

    def get_queryset(self):
        game_id = self.request.query_params.get("game")
        if game_id is not None:
            return models.RobotData.objects.filter(game=game_id)
        else:
            return models.RobotData.objects.all()

class ImageViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    queryset = models.Image.objects.all()
    serializer_class = serializers.ImageSerializer

    def list(self, request, *args, **kwargs):
        # Keep the original list behavior
        return super().list(request, *args, **kwargs)

    def get_queryset(self):
        log_id = self.request.query_params.get("log")
        camera = self.request.query_params.get('camera')
        print("log_id", log_id)
        if log_id is not None and camera is not None:
            queryset = models.Image.objects.filter(log=log_id, camera=camera)
        else:
            queryset = models.Image.objects.all()

        return queryset.order_by('frame_number')
    
    def create(self, request, *args, **kwargs):
        data = request.data  # This should be a list of dictionaries
        #print(data)
        if not isinstance(data, list):
            return Response({"error": "Data must be a list"}, status=status.HTTP_400_BAD_REQUEST)

        with transaction.atomic():
            # Fetch all relevant RobotData instances
            log_ids = set(item['log'] for item in data)
            robot_data_dict = {rd.id: rd for rd in models.RobotData.objects.filter(id__in=log_ids)}

            # Get existing objects
            existing_combinations = set(
                models.Image.objects.filter(
                    Q(log__in=log_ids) &
                    Q(camera__in=[item['camera'] for item in data]) &
                    Q(type__in=[item['type'] for item in data]) &
                    Q(frame_number__in=[item['frame_number'] for item in data])
                ).values_list('log', 'camera', 'type', 'frame_number')
            )


            # Prepare new objects, excluding existing combinations
            new_objs = []
            for item in data:
                log_instance = robot_data_dict.get(item['log'])
                if log_instance and (item['log'], item['camera'], item['type'], item['frame_number']) not in existing_combinations:
                    new_item = item.copy()
                    # Replace the log ID with the actual RobotData instance
                    new_item['log'] = log_instance
                    # Create a new Image instance with all provided fields
                    new_obj = models.Image(**new_item)
                    new_objs.append(new_obj)

            # Bulk create new objects, ignoring conflicts
            models.Image.objects.bulk_create(new_objs, ignore_conflicts=True)

            # Fetch all objects (both existing and newly created)
            all_objs = models.Image.objects.filter(
                Q(log__in=[item['log'] for item in data]) &
                Q(camera__in=[item['camera'] for item in data]) &
                Q(type__in=[item['type'] for item in data]) &
                Q(frame_number__in=[item['frame_number'] for item in data])
            )

            # Serialize the results
            serializer = self.serializer_class(all_objs, many=True)

            return Response(serializer.data, status=status.HTTP_201_CREATED)

class ImageCountView(APIView):
    def get(self, request):
        # Get filter parameters from query string
        log_id = request.query_params.get('log')
        camera = request.query_params.get('camera')
        image_type = request.query_params.get('type')

        # Start with all images
        queryset = models.Image.objects.all()

        # Apply filters if provided
        queryset = queryset.filter(log_id=log_id, camera=camera, type=image_type)

        # Get the count
        count = queryset.count()

        return Response({'count': count}, status=status.HTTP_200_OK)


class ImageAnnotationViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    queryset = models.ImageAnnotation.objects.all()
    serializer_class = serializers.ImageAnnotationSerializer