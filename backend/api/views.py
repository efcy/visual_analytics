from django.contrib.auth.models import User
from rest_framework import generics,viewsets
from .serializers import UserSerializer, EventSerializer,GameSerializer, LogSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Event,Game,Log

class EventViewSet(viewsets.ModelViewSet):
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


class GameViewSet(viewsets.ModelViewSet):
    queryset = Game.objects.all()
    serializer_class = GameSerializer
    def get_queryset(self):
        event_id = self.request.query_params.get("event")
        if event_id is not None:
            return Game.objects.filter(event=event_id)
        else:
            return Game.objects.all()
        

class LogViewSet(viewsets.ModelViewSet):
    queryset = Log.objects.all()
    serializer_class = LogSerializer


class CreateUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]