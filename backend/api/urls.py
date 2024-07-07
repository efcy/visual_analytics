from django.urls import path
from .views import EventList, EventDetail, NoteListCreate, NoteDelete


urlpatterns = [
    path("notes/", NoteListCreate.as_view(), name="note-list"),
    path("notes/delete/<int:pk>/", NoteDelete.as_view(), name="delete-note"),
    path('events/', EventList.as_view(), name="event-list"),
    path('events/<int:pk>/', EventDetail.as_view()),
]