
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status
from rest_framework import viewsets

from django.db import transaction
from django.db.models import Q
from django.db import connection
from psycopg2.extras import execute_values

import json
import time

from .. import serializers
from .. import models

class BehaviorFrameCountView(APIView):
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
    

class BehaviorSymbolCountView(APIView):
    def get(self, request):
        # Get filter parameters from query string
        log_id = request.query_params.get('log_id')

        # Start with all images
        queryset = models.XabslSymbolSparse.objects.all()

        # Apply filters if provided
        queryset = queryset.filter(log_id=log_id)

        # Get the count
        unique_frame_count = queryset.values('frame').distinct().count()

        return Response({'count': unique_frame_count}, status=status.HTTP_200_OK)


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
        """
            asssumes all data send is from the same log
        """
        validated_data = serializer.validated_data

        with transaction.atomic():
            batch_log_id = validated_data[0]['log_id'].id
            # Get all existing combinations given the log id
            existing_combinations = set(
                models.BehaviorOptionState.objects
                .filter(log_id=batch_log_id)
                .values_list('option_id','xabsl_internal_state_id', 'name')
            )

            # filter out duplicates
            new_data = []
            for item in validated_data:
                combo = (item['option_id'], item['xabsl_internal_state_id'], item['name'])
                if combo not in existing_combinations:
                    new_data.append(models.BehaviorOptionState(**item))
                    existing_combinations.add(combo)  # Add to set to catch duplicates within the input

            # Bulk create new events
            created_data = models.BehaviorOptionState.objects.bulk_create(new_data)

        return Response({
            'created': len(created_data),
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
        if not is_many:
            print("error: input not a list")
            return Response({}, status=status.HTTP_411_LENGTH_REQUIRED)

        starttime = time.time()

        #rows_tuples = [(row['log_id'], row['options_id'], row['active_state'], row['parent'], row['frame'], row['time'], row['time_of_execution'], row['state_time']) for row in request.data]
        rows_tuples = [(row['log_id'], row['options_id'], row['active_state'], row['frame']) for row in request.data]
        with connection.cursor() as cursor:
            query = """
            INSERT INTO api_behaviorframeoption (log_id_id, options_id_id, active_state_id, frame)
            VALUES %s
            ON CONFLICT (log_id_id, options_id_id, frame, active_state_id) DO NOTHING;
            """ 
            # rows is a list of tuples containing the data
            execute_values(cursor, query, rows_tuples, page_size=500)
        print( time.time() - starttime)
        return Response({
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


class XabslSymbolSparseViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.XabslSymbolSparseSerializer
    permission_classes = [IsAuthenticated]
    queryset = models.XabslSymbolSparse.objects.all()

    def get_queryset(self):
        queryset = models.XabslSymbolSparse.objects.all()
        query_params = self.request.query_params

        # FIXME combine with behaviorfull
        # FIXME filter does not seem to work because we now store json
        filters = Q()
        for field in models.XabslSymbolSparse._meta.fields:
            param_value = query_params.get(field.name)
            if param_value:
                filters &= Q(**{field.name: param_value})
        # FIXME built in pagination here, otherwise it could crash something if someone tries to get all representations without filtering
        return queryset.filter(filters)
    
    def create(self, request, *args, **kwargs):
        starttime = time.time()
        # FIXME should be for bulk insert
        data = self.request.data
        #rows_tuples = [( data['log_id'], data['frame'], json.dumps( data['data']) )]

        rows_tuples = [(
            row['log_id'], 
            row['frame'], 
            json.dumps( row['data']),
        ) for row in data]

        with connection.cursor() as cursor:
            query = """
            INSERT INTO api_xabslsymbolsparse(log_id_id, frame, data)
            VALUES %s
            ON CONFLICT (log_id_id, frame) DO NOTHING;
            """ 
            # rows is a list of tuples containing the data
            execute_values(cursor, query, rows_tuples, page_size=1000)
        print(time.time() - starttime)
        return Response({
        }, status=status.HTTP_200_OK)
    

class XabslSymbolCompleteViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.XabslSymbolSparseSerializer
    permission_classes = [IsAuthenticated]
    queryset = models.XabslSymbolComplete.objects.all()

    def get_queryset(self):
        queryset = models.XabslSymbolComplete.objects.all()
        query_params = self.request.query_params

        filters = Q()
        for field in models.XabslSymbolComplete._meta.fields:
            param_value = query_params.get(field.name)
            if param_value:
                filters &= Q(**{field.name: param_value})
        # FIXME built in pagination here, otherwise it could crash something if someone tries to get all representations without filtering
        return queryset.filter(filters)
    
    def create(self, request, *args, **kwargs):
        starttime = time.time()
        data = request.data['data']
        rows_tuples = [( data['log_id'], json.dumps( data['data']) )]

        with connection.cursor() as cursor:
            query = """
            INSERT INTO api_xabslsymbolcomplete(log_id_id, data)
            VALUES %s
            ON CONFLICT (log_id_id) DO NOTHING;
            """ 
            # rows is a list of tuples containing the data
            execute_values(cursor, query, rows_tuples, page_size=1000)
        print(time.time() - starttime)
        return Response({
        }, status=status.HTTP_200_OK)

class XabslSymbol(APIView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        """
        Returns the list of XabslSymbol where we check that everything that is not in Sparse is replaced with data from BehaviorComplete
        """
        # we get as inputs the log_id, symbol name and possibly the value
        # we could first check if the value matches the behavior complete value if not
        #   the easy way we can just return the xabslsymbolsparse table with filter for value
        # if the value matches the behaviorcomplete value we need to somehow create a table
        #   that contains all frames and then remove the frames where behavorsparse has something else