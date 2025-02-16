import graphene
from graphene_django import DjangoObjectType

from .models import Event,Game,Log
from django.core.exceptions import FieldDoesNotExist
from graphene import InputObjectType, String, Int, Float, Boolean
from django.db.models import Q

def apply_generic_filters(model, queryset, filters):
    if not filters:
        return queryset
    
    query = Q()
    for filter in filters:
        field_name = filter.field
        value = filter.value
        
        try:
            # Get the Django model field type
            model_field = model._meta.get_field(field_name)
        except FieldDoesNotExist:
            raise ValueError(f"Field '{field_name}' does not exist on model '{model.__name__}'")
        
        # Convert `value` to the correct type based on the model field
        try:
            typed_value = model_field.to_python(value)
        except Exception as e:
            raise ValueError(f"Invalid value '{value}' for field '{field_name}': {str(e)}")
        
        # Build the filter
        query &= Q(**{field_name: typed_value})
    
    return queryset.filter(query)


#test for generic filters 
#this is a type that contains a key value pair 
class GenericFilterInput(InputObjectType):
    field = String(required=True)
    value = String()

class EventType(DjangoObjectType):
    
    class Meta:
        model = Event
        fields = "__all__"

class GameType(DjangoObjectType):
    
    class Meta:
        model = Game
        fields = "__all__"

class LogType(DjangoObjectType):
    
    class Meta:
        model = Log
        fields = "__all__"

class CreateEvent(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
    
    event = graphene.Field(EventType)

    def mutate(self, info,name):
        event = Event(name=name)
        event.save()
        return CreateEvent(event=event)

class Query(graphene.ObjectType):
    #extra argument for each Type is a list of Filter Type so we can filter for multiple fields
    events = graphene.List(EventType, filters=graphene.List(GenericFilterInput))
    games = graphene.List(GameType, filters=graphene.List(GenericFilterInput))
    logs = graphene.List(LogType, filters=graphene.List(GenericFilterInput))

    def resolve_events(self, info, filters=None):
        user = info.context.user
        if not user.is_authenticated:
            raise graphene.PermissionDenied("Authentication required")
        queryset = Event.objects.all()    
        return apply_generic_filters(Event,queryset, filters)

    def resolve_games(self, info, filters=None):
        queryset = Game.objects.all()
        return apply_generic_filters(Game,queryset, filters)

    def resolve_logs(self, info, filters=None):
        queryset = Log.objects.all()
        return apply_generic_filters(Log,queryset, filters)
    

class Mutation(graphene.ObjectType):
    create_event = CreateEvent.Field()

schema = graphene.Schema(query=Query,mutation=Mutation)