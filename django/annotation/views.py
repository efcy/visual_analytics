from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Annotation
from .serializers import AnnotationSerializer


class AnnotationViewSet(viewsets.ModelViewSet):
    queryset = Annotation.objects.all()
    serializer_class = AnnotationSerializer
    
    def get_queryset(self):
        queryset = Annotation.objects.all()
        
        query_params = self.request.query_params.copy()
        
        if "id" in query_params:
            id_value = query_params["id"]
            queryset = queryset.filter(image__log=id_value)

        if "label" in query_params:
            label_value = query_params["label"]
            # Filter the queryset where the label in any of the bbox objects matches the provided label_value
            queryset = queryset.filter(annotation__bbox__contains=[{"label": label_value}])

        return queryset
        #image_id = self.request.query_params.get("image")
        #if image_id is not None:
        #    return queryset.filter(image=image_id).get()
        
        

    def retrieve(self, request, *args, **kwargs):
        # FIXME return empty response if no annotation is present
        # do your customization here
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        # FIXME remove the copied code and write a test for the sdk for generating annotations for a given image
        # Check if the data is a list (bulk create) or dict (single create)
        print(request.data)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data
        
        instance, created = Annotation.objects.get_or_create(
            image=validated_data.get('image_id'),
            annotation=validated_data.get('annotation'),
            defaults=validated_data
        )
        
        status_code = status.HTTP_201_CREATED if created else status.HTTP_200_OK
        
        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=status_code)