
from django.shortcuts import get_object_or_404
from rest_framework import generics,viewsets
from . import serializers
from django.db.models import F
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


class CreateUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer
    permission_classes = [AllowAny]

class EventViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.EventSerializer
    permission_classes = [IsAuthenticated]
    queryset = models.Event.objects.all()

    def get_queryset(self):
        return models.Event.objects.all()
    
    def create(self, request, *args, **kwargs):
        # Check if the data is a list (bulk create) or dict (single create)
        is_many = isinstance(request.data, list)
        
        serializer = self.get_serializer(data=request.data, many=is_many)
        serializer.is_valid(raise_exception=True)
        
        if is_many:
            return self.bulk_create(serializer)
        else:
            return self.single_create(serializer)

    def single_create(self, serializer):
        validated_data = serializer.validated_data
        
        instance, created = models.Event.objects.get_or_create(
            name=validated_data.get('name'),
            defaults=validated_data
        )
        
        status_code = status.HTTP_201_CREATED if created else status.HTTP_200_OK
        
        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=status_code)

    def bulk_create(self, serializer):
        validated_data = serializer.validated_data

        with transaction.atomic():
            # Get all existing names
            existing_names = set(models.Event.objects.filter(
                name__in=[item['name'] for item in validated_data]
            ).values_list('name', flat=True))

            # Separate new and existing events
            new_events = []
            existing_events = []
            for item in validated_data:
                if item['name'] not in existing_names:
                    new_events.append(models.Event(**item))
                    existing_names.add(item['name'])  # Add to set to catch duplicates within the input
                else:
                    existing_events.append(models.Event.objects.get(name=item['name']))

            # Bulk create new events
            created_events = models.Event.objects.bulk_create(new_events)

        # Combine created and existing events
        all_events = created_events + existing_events

        # Serialize the results
        result_serializer = self.get_serializer(all_events, many=True)

        return Response({
            'created': len(created_events),
            'existing': len(existing_events),
            'events': result_serializer.data
        }, status=status.HTTP_200_OK)


class GameViewSet(viewsets.ModelViewSet):
    queryset = models.Game.objects.all()
    serializer_class = serializers.GameSerializer
    permission_classes = [IsAuthenticated]
   
    def get_queryset(self):
        event_id = self.request.query_params.get("event")
        if event_id is not None:
            return models.Game.objects.filter(event_id=event_id)
        else:
            return models.Game.objects.all()
        
    def create(self, request, *args, **kwargs):
        # Check if the data is a list (bulk create) or dict (single create)
        is_many = isinstance(request.data, list)
        
        serializer = self.get_serializer(data=request.data, many=is_many)
        serializer.is_valid(raise_exception=True)
        
        if is_many:
            return self.bulk_create(serializer)
        else:
            return self.single_create(serializer)

    def single_create(self, serializer):
        validated_data = serializer.validated_data
        
        instance, created = models.Game.objects.get_or_create(
            event_id=validated_data.get('event_id'),
            start_time=validated_data.get('start_time'),
            half=validated_data.get('half'),
            defaults=validated_data
        )
        
        status_code = status.HTTP_201_CREATED if created else status.HTTP_200_OK
        
        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=status_code)

    def bulk_create(self, serializer):
        validated_data = serializer.validated_data

        with transaction.atomic():
            # Get all existing games
            existing_combinations = set(
                models.Game.objects.values_list('event_id', 'start_time', 'half')
            )

            # Separate new and existing events
            new_games = []
            existing_games = []
            for item in validated_data:
                combo = (item['event_id'], item['start_time'], item['half'])
                if combo not in existing_combinations:
                    new_games.append(models.Game(**item))
                    existing_combinations.add(combo)  # Add to set to catch duplicates within the input
                else:
                    # Fetch the existing event
                    existing_event = models.Game.objects.get(
                        event_id=item['event_id'],
                        start_time=item['start_time'],
                        half=item['half']
                    )
                    existing_games.append(existing_event)

            # Bulk create new events
            created_games = models.Game.objects.bulk_create(new_games)

        # Combine created and existing events
        all_games = created_games + existing_games

        # Serialize the results
        result_serializer = self.get_serializer(all_games, many=True)

        return Response({
            'created': len(created_games),
            'existing': len(existing_games),
            'events': result_serializer.data
        }, status=status.HTTP_200_OK)
        
class LogViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = models.Log.objects.all()
    serializer_class = serializers.LogSerializer

    def get_queryset(self):
        queryset = models.Log.objects.all()
        query_params = self.request.query_params

        filters = Q()
        for field in models.Log._meta.fields:
            param_value = query_params.get(field.name)
            if param_value:
                filters &= Q(**{field.name: param_value})

        return queryset.filter(filters)
        
    def create(self, request, *args, **kwargs):
        # Check if the data is a list (bulk create) or dict (single create)
        is_many = isinstance(request.data, list)
        
        serializer = self.get_serializer(data=request.data, many=is_many)
        serializer.is_valid(raise_exception=True)
        
        if is_many:
            return self.bulk_create(serializer)
        else:
            return self.single_create(serializer)

    def single_create(self, serializer):
        validated_data = serializer.validated_data
        
        instance, created = models.Log.objects.get_or_create(
            game_id=validated_data.get('game_id'),
            player_number=validated_data.get('player_number'),
            head_number=validated_data.get('head_number'),
            log_path=validated_data.get('log_path'),
            defaults=validated_data
        )
        
        status_code = status.HTTP_201_CREATED if created else status.HTTP_200_OK
        
        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=status_code)

    def bulk_create(self, serializer):
        validated_data = serializer.validated_data

        with transaction.atomic():
            # Get all existing logs
            existing_combinations = set(
                models.Log.objects.values_list('game_id', 'player_number', 'head_number', 'log_path')
            )

            # Separate new and existing events
            new_logs = []
            existing_logs = []
            for item in validated_data:
                combo = (item['game_id'], item['player_number'], item['head_number'], item['log_path'])
                if combo not in existing_combinations:
                    new_logs.append(models.Log(**item))
                    existing_combinations.add(combo)  # Add to set to catch duplicates within the input
                else:
                    # Fetch the existing event
                    existing_event = models.Log.objects.get(
                        game_id=item['game_id'],
                        player_number=item['player_number'],
                        head_number=item['head_number'],
                        log_path=item['log_path']
                    )
                    existing_logs.append(existing_event)

            # Bulk create new events
            created_logs = models.Log.objects.bulk_create(new_logs)

        # Combine created and existing events
        all_logs = created_logs + existing_logs

        # Serialize the results
        result_serializer = self.get_serializer(all_logs, many=True)

        return Response({
            'created': len(created_logs),
            'existing': len(existing_logs),
            'events': result_serializer.data
        }, status=status.HTTP_200_OK)

class ImageViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = models.Image.objects.all()
    serializer_class = serializers.ImageSerializer

    def get_queryset(self):
        queryset = models.Image.objects.all()
        query_params = self.request.query_params

        filters = Q()
        for field in models.Image._meta.fields:
            param_value = query_params.get(field.name)
            if param_value:
                filters &= Q(**{field.name: param_value})
        # FIXME built in pagination here, otherwise it could crash something if someone tries to get all representations without filtering
        return queryset.filter(filters).order_by('frame_number')
    
    def create(self, request, *args, **kwargs):
        # Check if the data is a list (bulk create) or dict (single create)
        is_many = isinstance(request.data, list)
        
        serializer = self.get_serializer(data=request.data, many=is_many)
        serializer.is_valid(raise_exception=True)
        
        if is_many:
            return self.bulk_create(serializer)
        else:
            return self.single_create(serializer)
        
    def single_create(self, serializer):
        validated_data = serializer.validated_data
        
        instance, created = models.Image.objects.get_or_create(
            log=validated_data.get('log'),
            camera=validated_data.get('camera'),
            type=validated_data.get('type'),
            frame_number=validated_data.get('frame_number'),
            defaults=validated_data
        )
        
        status_code = status.HTTP_201_CREATED if created else status.HTTP_200_OK
        
        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=status_code)    
    
    def bulk_create(self, serializer):
        validated_data = serializer.validated_data

        with transaction.atomic():
            # Get all existing games
            existing_combinations = set(
                models.Image.objects.values_list('log', 'camera', 'type', 'frame_number')
            )
            print(existing_combinations)
            # Separate new and existing events
            new_data = []
            existing_data = []
            for item in validated_data:
                # item['log_id'].id is needed because item['log_id'] gives a reference to the log object
                combo = (item['log'].id, item['camera'], item['type'], item['frame_number'])

                if combo not in existing_combinations:
                    new_data.append(models.Image(**item))
                    existing_combinations.add(combo)  # Add to set to catch duplicates within the input
                else:
                    print("\tfound existing data")
                    # Fetch the existing event
                    existing_event = models.Image.objects.get(
                        log=item['log'],
                        camera=item['camera'],
                        type=item['type'],
                        frame_number=item['frame_number']
                    )
                    existing_data.append(existing_event)

            # Bulk create new images
            created_data = models.Image.objects.bulk_create(new_data)

        # Combine created and existing events
        #all_data = created_data + existing_data

        # Serialize the results
        #result_serializer = self.get_serializer(all_data, many=True)

        return Response({
            'created': len(created_data),
            'existing': len(existing_data),
        #    'events': result_serializer.data
        }, status=status.HTTP_200_OK)

    """
    def create(self, request, *args, **kwargs):
        data = request.data  # This should be a list of dictionaries
        #print(data)
        if not isinstance(data, list):
            return Response({"error": "Data must be a list"}, status=status.HTTP_400_BAD_REQUEST)

        with transaction.atomic():
            # Fetch all relevant Log instances
            log_ids = set(item['log'] for item in data)
            robot_data_dict = {rd.id: rd for rd in models.Log.objects.filter(id__in=log_ids)}

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
    """

class ImageCountView(APIView):
    # TODO to I still need this?
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

class BehaviorCountView(APIView):
    def get(self, request):
        # Get filter parameters from query string
        log_id = request.query_params.get('log_id')

        # Start with all images
        queryset = models.BehaviorFrameOption.objects.all()

        # Apply filters if provided
        queryset = queryset.filter(log_id=log_id)

        # Get the count
        unique_frame_count = queryset.values('frame').distinct().count()

        return Response({'count': unique_frame_count}, status=status.HTTP_200_OK)

class CognitionRepresentationViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = models.CognitionRepresentation.objects.all()
    serializer_class = serializers.CognitionRepresentationSerializer

    def get_queryset(self):
        queryset = models.CognitionRepresentation.objects.all()
        query_params = self.request.query_params

        filters = Q()
        for field in models.CognitionRepresentation._meta.fields:
            param_value = query_params.get(field.name)
            if param_value:
                filters &= Q(**{field.name: param_value})
        # FIXME built in pagination here, otherwise it could crash something if someone tries to get all representations without filtering
        return queryset.filter(filters)

    def create(self, request, *args, **kwargs):
        # Check if the data is a list (bulk create) or dict (single create)
        is_many = isinstance(request.data, list)
        
        serializer = self.get_serializer(data=request.data, many=is_many)
        serializer.is_valid(raise_exception=True)
        
        if is_many:
            return self.bulk_create(serializer)
        else:
            return self.single_create(serializer)

    def single_create(self, serializer):
        validated_data = serializer.validated_data
        
        instance, created = models.CognitionRepresentation.objects.get_or_create(
            log_id=validated_data.get('log_id'),
            frame_number=validated_data.get('frame_number'),
            representation_name=validated_data.get('representation_name'),
            defaults=validated_data
        )
        
        status_code = status.HTTP_201_CREATED if created else status.HTTP_200_OK
        
        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=status_code)

    def bulk_create(self, serializer):
        validated_data = serializer.validated_data

        with transaction.atomic():
            # Get all existing games
            existing_combinations = set(
                models.CognitionRepresentation.objects.values_list('log_id', 'frame_number', 'representation_name')
            )
            print(existing_combinations)
            # Separate new and existing events
            new_data = []
            existing_data = []
            for item in validated_data:
                # item['log_id'].id is needed because item['log_id'] gives a reference to the log object
                combo = (item['log_id'].id, item['frame_number'], item['representation_name'])
                print(type(item['log_id']))
                print(item['log_id'].id)
                print(f"\tcombo: {combo}")
                if combo not in existing_combinations:
                    new_data.append(models.CognitionRepresentation(**item))
                    existing_combinations.add(combo)  # Add to set to catch duplicates within the input
                else:
                    print("\tfound existing data")
                    # Fetch the existing event
                    existing_event = models.CognitionRepresentation.objects.get(
                        log_id=item['log_id'],
                        frame_number=item['frame_number'],
                        representation_name=item['representation_name']
                    )
                    existing_data.append(existing_event)

            # Bulk create new events
            created_data = models.CognitionRepresentation.objects.bulk_create(new_data)

        # Combine created and existing events
        #all_data = created_data + existing_data

        # Serialize the results
        #result_serializer = self.get_serializer(all_data, many=True)

        return Response({
            'created': len(created_data),
            'existing': len(existing_data),
        #    'events': result_serializer.data
        }, status=status.HTTP_200_OK)
    
class MotionRepresentationViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.MotionRepresentationSerializer
    permission_classes = [IsAuthenticated]
    queryset = models.MotionRepresentation.objects.all()

    def get_queryset(self):
        queryset = models.MotionRepresentation.objects.all()
        query_params = self.request.query_params

        filters = Q()
        for field in models.MotionRepresentation._meta.fields:
            param_value = query_params.get(field.name)
            if param_value:
                filters &= Q(**{field.name: param_value})
        # FIXME built in pagination here, otherwise it could crash something if someone tries to get all representations without filtering
        return queryset.filter(filters)

    def create(self, request, *args, **kwargs):
        # Check if the data is a list (bulk create) or dict (single create)
        is_many = isinstance(request.data, list)
        
        serializer = self.get_serializer(data=request.data, many=is_many)
        serializer.is_valid(raise_exception=True)
        
        if is_many:
            return self.bulk_create(serializer)
        else:
            return self.single_create(serializer)

    def single_create(self, serializer):
        validated_data = serializer.validated_data
        
        instance, created = models.MotionRepresentation.objects.get_or_create(
            log_id=validated_data.get('log_id'),
            sensor_frame_number=validated_data.get('sensor_frame_number'),
            representation_name=validated_data.get('representation_name'),
            defaults=validated_data
        )
        
        status_code = status.HTTP_201_CREATED if created else status.HTTP_200_OK
        
        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=status_code)

    def bulk_create(self, serializer):
        validated_data = serializer.validated_data

        with transaction.atomic():
            # Get all existing games
            existing_combinations = set(
                models.MotionRepresentation.objects.values_list('log_id', 'sensor_frame_number', 'representation_name')
            )

            # Separate new and existing events
            new_data = []
            existing_data = []
            for item in validated_data:
                combo = (item['log_id'].id, item['sensor_frame_number'], item['representation_name'])
                if combo not in existing_combinations:
                    new_data.append(models.MotionRepresentation(**item))
                    existing_combinations.add(combo)  # Add to set to catch duplicates within the input
                else:
                    # Fetch the existing event
                    existing_event = models.MotionRepresentation.objects.get(
                        log_id=item['log_id'],
                        sensor_frame_number=item['sensor_frame_number'],
                        representation_name=item['representation_name']
                    )
                    existing_data.append(existing_event)

            # Bulk create new events
            created_data = models.MotionRepresentation.objects.bulk_create(new_data)

        # Combine created and existing events
        all_data = created_data + existing_data

        # Serialize the results
        result_serializer = self.get_serializer(all_data, many=True)

        return Response({
            'created': len(created_data),
            'existing': len(existing_data),
            'events': result_serializer.data
        }, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        # Override destroy method to handle both single and bulk delete
        if kwargs.get('pk') == 'all':
            deleted_count, _ = self.get_queryset().delete()
            return Response({'message': f'Deleted {deleted_count} objects'}, status=status.HTTP_204_NO_CONTENT)
        return super().destroy(request, *args, **kwargs)


class BehaviorOptionViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.BehaviorOptionSerializer
    permission_classes = [IsAuthenticated]
    queryset = models.BehaviorOption.objects.all()

    def get_queryset(self):
        queryset = models.BehaviorOption.objects.all()
        query_params = self.request.query_params

        filters = Q()
        for field in models.BehaviorOption._meta.fields:
            param_value = query_params.get(field.name)
            if param_value:
                filters &= Q(**{field.name: param_value})
        # FIXME built in pagination here, otherwise it could crash something if someone tries to get all representations without filtering
        return queryset.filter(filters)
    
    def create(self, request, *args, **kwargs):
        # Check if the data is a list (bulk create) or dict (single create)
        is_many = isinstance(request.data, list)
        
        serializer = self.get_serializer(data=request.data, many=is_many)
        serializer.is_valid(raise_exception=True)
        
        if is_many:
            return self.bulk_create(serializer)
        else:
            return self.single_create(serializer)

    def single_create(self, serializer):
        validated_data = serializer.validated_data
        
        instance, created = models.BehaviorOption.objects.get_or_create(
            log_id=validated_data.get('log_id'),
            xabsl_internal_option_id=validated_data.get('xabsl_internal_option_id'),
            option_name=validated_data.get('option_name'),
            defaults=validated_data
        )
        
        status_code = status.HTTP_201_CREATED if created else status.HTTP_200_OK
        
        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=status_code)

    def bulk_create(self, serializer):
        validated_data = serializer.validated_data

        with transaction.atomic():
            # Get all existing games
            existing_combinations = set(
                models.BehaviorOption.objects.values_list('log_id', 'option_name', 'xabsl_internal_option_id')
            )

            # Separate new and existing events
            new_data = []
            existing_data = []
            for item in validated_data:
                combo = (item['log_id'].id, item['option_name'], item['xabsl_internal_option_id'])
                if combo not in existing_combinations:
                    new_data.append(models.BehaviorOption(**item))
                    existing_combinations.add(combo)  # Add to set to catch duplicates within the input
                else:
                    # Fetch the existing event
                    existing_event = models.BehaviorOption.objects.get(
                        log_id=item['log_id'],
                        option_name=item['option_name'],
                        xabsl_internal_option_id=item['xabsl_internal_option_id'],
                    )
                    existing_data.append(existing_event)

            # Bulk create new events
            created_data = models.BehaviorOption.objects.bulk_create(new_data)

        # Combine created and existing events
        all_data = created_data + existing_data

        # Serialize the results
        result_serializer = self.get_serializer(all_data, many=True)

        return Response({
            'created': len(created_data),
            'existing': len(existing_data),
            'events': result_serializer.data
        }, status=status.HTTP_200_OK)

class BehaviorOptionStateViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.BehaviorOptionsStateSerializer
    permission_classes = [IsAuthenticated]
    queryset = models.BehaviorOptionState.objects.all()

    def get_queryset(self):
        queryset = models.BehaviorOptionState.objects.all()
        query_params = self.request.query_params

        filters = Q()
        for field in models.BehaviorOptionState._meta.fields:
            param_value = query_params.get(field.name)
            if param_value:
                filters &= Q(**{field.name: param_value})
        # FIXME built in pagination here, otherwise it could crash something if someone tries to get all representations without filtering
        return queryset.filter(filters)
    
    def create(self, request, *args, **kwargs):
        # Check if the data is a list (bulk create) or dict (single create)
        is_many = isinstance(request.data, list)
        
        serializer = self.get_serializer(data=request.data, many=is_many)
        serializer.is_valid(raise_exception=True)
        
        if is_many:
            return self.bulk_create(serializer)
        else:
            return self.single_create(serializer)

    def single_create(self, serializer):
        validated_data = serializer.validated_data
        
        instance, created = models.BehaviorOptionState.objects.get_or_create(
            log_id=validated_data.get('log_id'),
            option_id=validated_data.get('option_id'),
            xabsl_internal_state_id=validated_data.get('xabsl_internal_state_id'),
            name=validated_data.get('name'),
            defaults=validated_data
        )
        
        status_code = status.HTTP_201_CREATED if created else status.HTTP_200_OK
        
        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=status_code)

    def bulk_create(self, serializer):
        validated_data = serializer.validated_data

        with transaction.atomic():
            # Get all existing games
            existing_combinations = set(
                models.BehaviorOptionState.objects.values_list('log_id', 'option_id','xabsl_internal_state_id', 'name')
            )

            # Separate new and existing events
            new_data = []
            existing_data = []
            for item in validated_data:
                combo = (item['log_id'].id, item['option_id'], item['xabsl_internal_state_id'], item['name'])
                if combo not in existing_combinations:
                    new_data.append(models.BehaviorOptionState(**item))
                    existing_combinations.add(combo)  # Add to set to catch duplicates within the input
                else:
                    # Fetch the existing event
                    existing_event = models.BehaviorOptionState.objects.get(
                        log_id=item['log_id'],
                        option_id=item['option_id'],
                        xabsl_internal_state_id=item['xabsl_internal_state_id'],
                        name=item['name'],
                    )
                    existing_data.append(existing_event)

            # Bulk create new events
            created_data = models.BehaviorOptionState.objects.bulk_create(new_data)

        # Combine created and existing events
        all_data = created_data + existing_data

        # Serialize the results
        result_serializer = self.get_serializer(all_data, many=True)

        return Response({
            'created': len(created_data),
            'existing': len(existing_data),
            'events': result_serializer.data
        }, status=status.HTTP_200_OK)
 
class BehaviorFrameOptionViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.BehaviorFrameOptionSerializer
    permission_classes = [IsAuthenticated]
    queryset = models.BehaviorFrameOption.objects.all()

    def get_queryset(self):
        queryset = models.BehaviorFrameOption.objects.all()
        query_params = self.request.query_params

        filters = Q()
        for field in models.BehaviorFrameOption._meta.fields:
            param_value = query_params.get(field.name)
            if param_value:
                filters &= Q(**{field.name: param_value})
        # FIXME built in pagination here, otherwise it could crash something if someone tries to get all representations without filtering
        return queryset.filter(filters)
    
    def create(self, request, *args, **kwargs):
        # Check if the data is a list (bulk create) or dict (single create)
        is_many = isinstance(request.data, list)
        
        serializer = self.get_serializer(data=request.data, many=is_many)
        serializer.is_valid(raise_exception=True)
        
        if is_many:
            return self.bulk_create(serializer)
        else:
            return self.single_create(serializer)

    def single_create(self, serializer):
        validated_data = serializer.validated_data
        
        instance, created = models.BehaviorFrameOption.objects.get_or_create(
            log_id=validated_data.get('log_id'),
            options_id=validated_data.get('options_id'),
            frame=validated_data.get('frame'),
            defaults=validated_data
        )
        
        status_code = status.HTTP_201_CREATED if created else status.HTTP_200_OK
        
        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=status_code)

    def bulk_create(self, serializer):
        validated_data = serializer.validated_data

        with transaction.atomic():
            # Get all existing games
            existing_combinations = set(
                models.BehaviorFrameOption.objects.values_list('log_id', 'options_id', 'frame')
            )

            # Separate new and existing events
            new_data = []
            existing_data = []
            for item in validated_data:
                combo = (item['log_id'].id, item['options_id'], item['frame'])
                if combo not in existing_combinations:
                    new_data.append(models.BehaviorFrameOption(**item))
                    existing_combinations.add(combo)  # Add to set to catch duplicates within the input
                else:
                    # Fetch the existing event
                    existing_event = models.BehaviorFrameOption.objects.get(
                        log_id=item['log_id'],
                        options_id=item['options_id'],
                        frame=item['frame'],
                    )
                    existing_data.append(existing_event)

            # Bulk create new events
            created_data = models.BehaviorFrameOption.objects.bulk_create(new_data)

        # Combine created and existing events
        all_data = created_data + existing_data

        # Serialize the results
        result_serializer = self.get_serializer(all_data, many=True)

        return Response({
            'created': len(created_data),
            'existing': len(existing_data),
            'events': result_serializer.data
        }, status=status.HTTP_200_OK)
    

class BehaviorFrameOptionAPIView(APIView):
    permission_classes = [AllowAny]
    def get(self, request, *args, **kwargs):
        # Get the log_id from the query parameters
        log_id = request.query_params.get('log_id')
        option_name = request.query_params.get('option_name')
        state_name = request.query_params.get('state_name')

        if not log_id or not option_name or not state_name:
            return Response({"error": "not all required parameter were provided"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Filter the BehaviorFrameOption records by the log_id
            behavior_frame_options =  models.BehaviorFrameOption.objects.select_related(
                'options_id',         # Joins BehaviorOption
                'active_state',       # Joins BehaviorOptionState
                'active_state__option_id'  # Joins BehaviorOption via BehaviorOptionState
            ).filter(log_id=log_id, options_id__option_name=option_name, active_state__name=state_name)

            # Serialize the data
            serializer = serializers.BehaviorFrameOptionCustomSerializer(behavior_frame_options, many=True)

            # Return the serialized data
            return Response(serializer.data)
        except ValueError:
            return Response({"error": "Invalid log_id."}, status=status.HTTP_400_BAD_REQUEST)
