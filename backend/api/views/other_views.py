
from rest_framework import generics,viewsets
from rest_framework import permissions
from . import serializers
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from . import models
from django.http import JsonResponse,HttpResponse
from django.views.decorators.http import require_GET
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import Q,F,functions, Value, CharField,Count
import time
import json
from django.db import connection
from psycopg2.extras import execute_values
from django.db.models import Count
from drf_spectacular.utils import extend_schema,extend_schema_view,OpenApiResponse,inline_serializer,OpenApiExample
from rest_framework import serializers as s
from django.template import loader

User = get_user_model()


@require_GET
def scalar_doc(request):
    template = loader.get_template("api/api_scalar.html")
    return HttpResponse(template.render())

@require_GET
def health_check(request):
    return JsonResponse({"message": "UP"}, status=200)


class CreateUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer
    permission_classes = [AllowAny]

# we use tags to group endpoints and sort them by order in settings.py
@extend_schema( tags = ['Events'])
@extend_schema_view(
    list= extend_schema(
       description='List all events',
       responses={200: serializers.EventSerializer(many=True)}
   )
)
class EventViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.EventSerializer
    queryset = models.Event.objects.all()

    @extend_schema(
       description='Create single or multiple events',
       request=serializers.EventSerializer(many=True),
       # Example data for test requests 
       examples=[
            OpenApiExample(
                'Single Event Creation',
                value={'name': 'Conference 2024', 'date': '2024-12-25'},
                request_only=True,
                summary='Create one event',
                description=''
            ),
            OpenApiExample(
                'Bulk Event Creation',
                value=[
                    {'name': 'Conference 2024', 'date': '2024-12-25'},
                    {'name': 'Workshop 2024', 'date': '2024-12-26'}
                ],
                request_only=True,
                summary='Create multiple events',
                )
        ],
       #displaying responses for single and bulk create but only response schema for single create 
       responses={
    201: OpenApiResponse(
        # response=[
        #     inline_serializer(
        #         name='BulkEventResponse',
        #         fields={
        #             'created': s.IntegerField(),
        #             'existing': s.IntegerField(),
        #             'events': serializers.EventSerializer(many=True)
        #         }
        #     ),
        #     serializers.EventSerializer],
        response = serializers.EventSerializer,
        
        description='Response for single or bulk create',
        examples=[
            OpenApiExample(
                name="Response for bulk create",
                value={
                    "created": 2,
                    "existing": 0,
                    "events": [
                        {"id": 1, "name": "Event 1", "date": "2024-12-23"},
                        {"id": 2, "name": "Event 2", "date": "2024-12-24"}
                    ]
                }
            ),
            OpenApiExample(
                name="Response for single create",
                value={
                    "id": 1,
                    "name": "Event 1",
                    "date": "2024-12-23"
                }
            )
        ]
    )
}
   )
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

        status_code = status.HTTP_201_CREATED if existing ==0 else status.HTTP_200_OK

        return Response({
            'created': len(created_events),
            'existing': len(existing_events),
            'events': result_serializer.data
        }, status=status_code)


class GameViewSet(viewsets.ModelViewSet):
    queryset = models.Game.objects.all()
    serializer_class = serializers.GameSerializer
   
    def get_queryset(self):
        event_id = self.request.query_params.get("event")

        queryset = models.Game.objects.select_related('event_id').annotate(event_name=F('event_id__name'))
        print(queryset.first().event_name)
        if event_id is not None:
            queryset = queryset.filter(event_id=event_id)
        
        return queryset
        
    def create(self, request, *args, **kwargs):
        row_tuple = [(
            request.data.get('event_id'),
            request.data.get('team1'),
            request.data.get('team2'),
            request.data.get('half'),
            request.data.get('is_testgame'),
            request.data.get('head_ref'),
            request.data.get('assistent_ref'),
            request.data.get('field'),
            request.data.get('start_time'),
            request.data.get('score'),
            request.data.get('comment'),
        )]
        with connection.cursor() as cursor:
            query = """
            INSERT INTO api_game (event_id_id, team1, team2, half, is_testgame, head_ref, assistent_ref, field, start_time, score, comment)
            VALUES %s
            ON CONFLICT (event_id_id, start_time, half) DO NOTHING
            RETURNING id;
            """

            execute_values(cursor, query, row_tuple, page_size=1)
            result = cursor.fetchone()
            if result:
                serializer = self.get_serializer(models.Game.objects.get(id=result[0]))
                # If insert was successful, get the object
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                # If ON CONFLICT DO NOTHING prevented insert, get the existing object
                instance = models.Game.objects.get(
                    event_id=request.data.get('event_id'),
                    start_time=request.data.get('start_time'),
                    half=request.data.get('half')
                )
                serializer = self.get_serializer(instance)

                return Response(serializer.data, status=status.HTTP_200_OK)


class LogViewSet(viewsets.ModelViewSet):
    queryset = models.Log.objects.all()
    serializer_class = serializers.LogSerializer

    def get_queryset(self):

        queryset = models.Log.objects.select_related('game_id').annotate(event_name=F('game_id__event_id__name'))

        queryset = queryset.select_related('game_id').annotate(game_name=functions.Concat(
        'game_id__start_time', Value(' '),
        'game_id__team1', Value(' vs '),
        'game_id__team2', Value(' '),
        'game_id__half',
        output_field=CharField()
    ))
         
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


class AnnotationViewSet(viewsets.ModelViewSet):
    queryset = models.Annotation.objects.all()
    serializer_class = serializers.AnnotationSerializer

    def create(self, request, *args, **kwargs):
        # Check if the data is a list (bulk create) or dict (single create)
        print(request.data)

class CognitionRepresentationViewSet(viewsets.ModelViewSet):
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
        if not is_many:
            print("error: input not a list")
            return Response({}, status=status.HTTP_411_LENGTH_REQUIRED)

        starttime = time.time()

        rows_tuples = [(row['log_id'], row['frame_number'], row['representation_name'], json.dumps(row['representation_data'])) for row in request.data]

        with connection.cursor() as cursor:
            query = """
            INSERT INTO api_cognitionrepresentation (log_id_id, frame_number, representation_name, representation_data)
            VALUES %s
            ON CONFLICT (log_id_id, frame_number, representation_name) DO UPDATE SET representation_data = EXCLUDED.representation_data;;
            """ 
            # rows is a list of tuples containing the data
            execute_values(cursor, query, rows_tuples, page_size=500)
        print( time.time() - starttime)
        return Response({
        }, status=status.HTTP_200_OK)


class CognitionReprCountView(APIView):
    def get(self, request):
        # Get filter parameters from query string
        log_id = request.query_params.get('log_id')

        # start with all images
        queryset = models.CognitionRepresentation.objects.all()

        # apply filters if provided
        queryset = queryset.filter(log_id=log_id)
        grouped_counts = queryset.values('representation_name').annotate(count=Count('id'))

        for group in grouped_counts:
            print(f"{group['representation_name']}: {group['count']}")
        # get the count
        result = {
            item['representation_name']: item['count'] 
            for item in grouped_counts
        }
        
        return Response(result, status=status.HTTP_200_OK)


class MotionRepresentationViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.MotionRepresentationSerializer
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
        if not is_many:
            print("error: input not a list")
            return Response({}, status=status.HTTP_411_LENGTH_REQUIRED)

        starttime = time.time()

        rows_tuples = [(row['log_id'], row['sensor_frame_number'], row['sensor_frame_time'], row['representation_name'], json.dumps(row['representation_data'])) for row in request.data]

        with connection.cursor() as cursor:
            query = """
            INSERT INTO api_motionrepresentation (log_id_id, sensor_frame_number, sensor_frame_time, representation_name, representation_data)
            VALUES %s
            ON CONFLICT (log_id_id, sensor_frame_number, representation_name) DO NOTHING;
            """ 
            # rows is a list of tuples containing the data
            execute_values(cursor, query, rows_tuples, page_size=500)
        print( time.time() - starttime)
        return Response({
        }, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        # Override destroy method to handle both single and bulk delete
        if kwargs.get('pk') == 'all':
            deleted_count, _ = self.get_queryset().delete()
            return Response({'message': f'Deleted {deleted_count} objects'}, status=status.HTTP_204_NO_CONTENT)
        return super().destroy(request, *args, **kwargs)


class MotionReprCountView(APIView):
    def get(self, request):
        # Get filter parameters from query string
        log_id = request.query_params.get('log_id')

        # start with all images
        queryset = models.MotionRepresentation.objects.all()

        # apply filters if provided
        queryset = queryset.filter(log_id=log_id)
        grouped_counts = queryset.values('representation_name').annotate(count=Count('id'))

        for group in grouped_counts:
            print(f"{group['representation_name']}: {group['count']}")
        # get the count
        result = {
            item['representation_name']: item['count'] 
            for item in grouped_counts
        }
        
        return Response(result, status=status.HTTP_200_OK)


class LogStatusViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.LogStatusSerializer
    queryset = models.LogStatus.objects.all()

    def get_queryset(self):
        return models.LogStatus.objects.all()
    
    def get_queryset(self):
        queryset = models.LogStatus.objects.all()
        query_params = self.request.query_params

        filters = Q()
        for field in models.LogStatus._meta.fields:
            param_value = query_params.get(field.name)
            if param_value:
                filters &= Q(**{field.name: param_value})
        # FIXME built in pagination here, otherwise it could crash something if someone tries to get all representations without filtering
        return queryset.filter(filters)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        validated_data = serializer.validated_data
        
        instance, created = models.LogStatus.objects.update_or_create(
            log_id=validated_data.get('log_id'),
            defaults=validated_data
        )
        
        status_code = status.HTTP_201_CREATED if created else status.HTTP_200_OK
        
        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=status_code)

class FrameFilterView(viewsets.ModelViewSet):
    serializer_class = serializers.FrameFilterSerializer
    queryset = models.FrameFilter.objects.all()

    def get_serializer_context(self):
        context = super().get_serializer_context()
        # Make sure the request is available in the serializer context
        return context

    def perform_create(self, serializer):
        serializer.save()  
