from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework import viewsets

from django.db import transaction
from django.db.models import Q
from django.db import connection
from psycopg2.extras import execute_values

from .. import serializers
from .. import models

import time

class ImageCountView(APIView):
    def get(self, request):
        # Get filter parameters from query string
        log_id = request.query_params.get('log')
        camera = request.query_params.get('camera')
        image_type = request.query_params.get('type')

        # start with all images
        queryset = models.Image.objects.all()

        # apply filters if provided
        queryset = queryset.filter(log_id=log_id, camera=camera, type=image_type)

        # get the count
        count = queryset.count()

        return Response({'count': count}, status=status.HTTP_200_OK)


class ImageViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = models.Image.objects.all()
    serializer_class = serializers.ImageSerializer

    def get_queryset(self):
        queryset = models.Image.objects.all()
        # we use copy here so that the QueryDict object query_params become mutable
        query_params = self.request.query_params.copy()

        # check if the frontend wants to use a frame filter
        if "use_filter" in query_params:
            # TODO check if we have a list of frames set here -> implement a model for this
            bla = True
            # we remove the frame filter query param for the QueryDict so that we can parse the rest of the filters normaly
            query_params.pop('use_filter')

        frame_numbers = [19108, 19109, 19110, 19111, 19112, 19113, 19114, 19115, 19116, 19117]
        # This is a generic filter on the queryset, the supplied filter must be a field in the Image model
        filters = Q()
        for field in models.Image._meta.fields:
            param_value = query_params.get(field.name)
            if param_value:
                filters &= Q(**{field.name: param_value})
        # FIXME built in pagination here, otherwise it could crash something if someone tries to get all representations without filtering
        qs = queryset.filter(filters).order_by('frame_number')
        if bla:
            qs = qs.filter(frame_number__in=frame_numbers)
        #return queryset.filter(filters).filter(frame_number__in=frame_numbers).order_by('frame_number')
        return qs.order_by('frame_number')
    
    def create(self, request, *args, **kwargs):
        # Check if the data is a list (bulk create) or dict (single create)
        is_many = isinstance(request.data, list)
        
        if is_many:
            return self.bulk_create(request.data)
        else:
            return self.single_create(request.data)

    def update(self, request, *args, **kwargs):
        # Check if the data is a list (bulk update) or dict (single update)
        is_many = isinstance(request.data, list)
        if is_many:
            return self.bulk_update()
        else:
            return self.single_update()

    def single_update(self):
        image_id = self.kwargs['pk']  # image id from the url: /api/image/17018/
        data = self.request.data
        
        # we ignore the fields that act as unique identifiers here
        update_fields = {k: v for k, v in data.items() if k not in ['log', 'camera', 'type', 'frame_number']}
        updated = models.Image.objects.filter(id=image_id).update(**update_fields)

        status_code = status.HTTP_201_CREATED if updated else status.HTTP_200_OK
        return Response({}, status=status_code)

    def bulk_update(self):
        # TODO implement me
        pass
        
    def single_create(self, data):
        serializer = self.get_serializer(data, many=False)
        serializer.is_valid(raise_exception=True)
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
    
    def bulk_create(self, data):
        #validated_data = serializer.validated_data
        starttime = time.time()
        rows_tuples = [(
            row['log'], 
            row['camera'], 
            row['type'], 
            row['frame_number'],
            row['image_url'],
            row['blurredness_value'],
            row['brightness_value'],
            row['resolution'],
            ) for row in data]
        with connection.cursor() as cursor:
            query = """
            INSERT INTO api_image (log_id, camera, type, frame_number, image_url, blurredness_value, brightness_value, resolution)
            VALUES %s
            ON CONFLICT (log_id, camera, type, frame_number) DO NOTHING;
            """ 
            # rows is a list of tuples containing the data
            execute_values(cursor, query, rows_tuples, page_size=1000)
        print( time.time() - starttime)
        # TODO calculate some statistics similar to what we did before here
        return Response({"message": "blabla"}, status=status.HTTP_200_OK)
        """
        with transaction.atomic():
            # Get all existing games
            existing_combinations = set(
                models.Image.objects.values_list('log', 'camera', 'type', 'frame_number')
            )
            #print(existing_combinations)
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


        return Response({
            'created': len(created_data),
            'existing': len(existing_data),
        #    'events': result_serializer.data
        }, status=status.HTTP_200_OK)
    """