from django.shortcuts import render, redirect
from django.views.generic import TemplateView, DetailView
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

from .forms import SignupForm
from api.models import Event, Game, Log, Image, CognitionRepresentation

def LoginView(request):
    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("events")
        else:
            messages.info(request, "Username or password is incorrect")

    context = {}
    return render(request, 'frontend/login.html', context)

def SignupView(request):
    form = SignupForm()
    context = {'form':form}

    if request.method == 'POST':
        form = SignupForm(request.POST)

        if form.is_valid():
            form.save()
            user = form.cleaned_data.get("username")
            messages.success(request, "Account was created for " + user)
            return redirect("login")
    
    context = {'form':form}
    return render(request, 'frontend/signup.html', context)

class EventListView(TemplateView):
    template_name = 'frontend/events.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['events'] = Event.objects.all()
        return context


class GameListView(DetailView):
    # could also be called EventDetailView
    model = Event
    template_name = 'frontend/games.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['games'] = Game.objects.filter(event_id=context['event'])
        
        return context

class LogListView(DetailView):
    # could also be called GameDetailView
    model = Game
    template_name = 'frontend/logs.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['logs'] = Log.objects.filter(game_id=context['game'])
        
        return context


class ImageListView(DetailView):
    # could also be called LogDetailView
    # TODO: maybe I should query FrameInfo from cognition representation table here sort that use that as extra parameter
    model = Log
    template_name = 'frontend/image.html'


    def get(self, request, *args, **kwargs):
        self.object = self.get_object()

        top_images = Image.objects.filter(log_id=self.object, camera="TOP").order_by('frame_number')
        if top_images.exists():
            first_image = top_images.first()

            return redirect('image_detail', pk=self.object.id, bla=first_image.frame_number)
        # TODO what if no images exist for a log -> redirect somewhere else
        return super().get(request, *args, **kwargs)  # Handle cases where no images exist


class ImageDetailView(DetailView):
    model = Image
    template_name = 'frontend/image_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        log_id = self.kwargs.get('pk')
        current_frame = self.kwargs.get('bla')
        context['bottom_image'] = Image.objects.filter(log_id=log_id, camera="BOTTOM", frame_number=current_frame).first()
        context['top_image'] = Image.objects.filter(log=log_id, camera="TOP", frame_number=current_frame).first()
        context['log_id'] = log_id
        context['frame_numbers'] = Image.objects.filter(log=log_id, camera="TOP").order_by('frame_number').values_list('frame_number', flat=True)

        return context