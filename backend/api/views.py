from django.contrib.auth.models import User
from rest_framework import generics
from .serializers import UserSerializer, EventSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Event

class EventList(generics.ListCreateAPIView):
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated]
    queryset = Event.objects.all()

    def get_queryset(self):
        """
        this is for the event search bar, maybe I can do this better/faster and with less database querying
        However this should never be that slow since we wont have that many events anyway
        """
        qs = Event.objects.all()
        name = self.request.query_params.get("name")

        if name is not None:
            qs = qs.filter(name__icontains=name)
        return qs


class EventDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated]
    queryset = Event.objects.all()


class CreateUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]