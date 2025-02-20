from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import CognitionFrame
from . import serializers

from django.db import connection
from django.db.models import Q

from psycopg2.extras import execute_values

# Create your views here.
class CognitionFrameCount(APIView):
    def get(self, request):
        # Get filter parameters from query string
        log_id = request.query_params.get('log_id')

        # start with all images
        queryset = CognitionFrame.objects.all()

        # apply filters if provided
        queryset = queryset.filter(log_id=log_id)

        # get the count
        count = queryset.count()
        return Response({'count': count}, status=status.HTTP_200_OK)
    

class CognitionFrameViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.CognitionFrameSerializer
    queryset = CognitionFrame.objects.all()

    def get_queryset(self):
        queryset = CognitionFrame.objects.all()
        query_params = self.request.query_params

        filters = Q()
        for field in CognitionFrame._meta.fields:
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

        rows_tuples = [(row['log_id'], row['frame_number'], row['frame_time']) for row in request.data]

        with connection.cursor() as cursor:
            query = """
            INSERT INTO cognition_cognitionframe (log_id_id, frame_number, frame_time)
            VALUES %s
            ON CONFLICT (log_id_id, frame_number) DO NOTHING;
            """ 
            # rows is a list of tuples containing the data
            execute_values(cursor, query, rows_tuples, page_size=500)

        return Response({
        }, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        # Override destroy method to handle both single and bulk delete
        if kwargs.get('pk') == 'all':
            deleted_count, _ = self.get_queryset().delete()
            return Response({'message': f'Deleted {deleted_count} objects'}, status=status.HTTP_204_NO_CONTENT)
        return super().destroy(request, *args, **kwargs)