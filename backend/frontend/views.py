from django.shortcuts import render, redirect
from django.views.generic import TemplateView, DetailView, View
from django.contrib.contenttypes.models import ContentType
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
import json
from .forms import SignupForm
from api.models import Event, Game, Log, Image, Annotation, FrameFilter, BehaviorFrameOption
from api.serializers import AnnotationSerializer
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework import status

def LoginView(request):
    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            next_url = request.GET.get("next", "events")
            return redirect(next_url)
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
            return redirect("mylogin")
    
    context = {'form':form}
    return render(request, 'frontend/signup.html', context)

def LogoutView(request):
    logout(request)
    return redirect('mylogin')



@method_decorator(login_required(login_url='mylogin'), name='dispatch')
class EventListView(TemplateView):
    template_name = 'frontend/events.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['events'] = Event.objects.all()
        return context


@method_decorator(login_required(login_url='mylogin'), name='dispatch')
class GameListView(DetailView):
    # could also be called EventDetailView
    model = Event
    template_name = 'frontend/games.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['games'] = Game.objects.filter(event_id=context['event'])
        
        return context


@method_decorator(login_required(login_url='mylogin'), name='dispatch')
class LogListView(DetailView):
    # could also be called GameDetailView
    model = Game
    template_name = 'frontend/logs.html'

    def get_context_data(self, **kwargs):
        game_content_type = ContentType.objects.get_for_model(Game)
        context = super().get_context_data(**kwargs)
        context['logs'] = Log.objects.filter(content_type=game_content_type, object_id=context['game'].id)
        
        return context


@method_decorator(login_required(login_url='mylogin'), name='dispatch')
class ImageListView(DetailView):
    # could also be called LogDetailView
    # TODO: maybe I should query FrameInfo from cognition representation table here sort that use that as extra parameter
    model = Log
    template_name = 'frontend/image.html'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()

        frames = FrameFilter.objects.filter(
            log_id=self.object,
            user=self.request.user,
        ).first()

        if frames:
            first_image = Image.objects.filter(log_id=self.object, frame_number__in=frames.frames["frame_list"]).order_by('frame_number').first()
        else:
            first_image = Image.objects.filter(log_id=self.object).order_by('frame_number').first()
        
        if first_image:        
            return redirect('image_detail', pk=self.object.id, bla=first_image.frame_number)
        # TODO what if no images exist for a log -> redirect somewhere else
        return super().get(request, *args, **kwargs)  # Handle cases where no images exist


@method_decorator(login_required(login_url='mylogin'), name='dispatch')
class ImageDetailView(View):
    def get(self, request, **kwargs):
        context = {}
        log_id = self.kwargs.get('pk')

        current_frame = self.kwargs.get('bla')
        context['bottom_image'] = Image.objects.filter(log_id=log_id, camera="BOTTOM", frame_number=current_frame).first()
        context['top_image'] = Image.objects.filter(log_id=log_id, camera="TOP", frame_number=current_frame).first()
        context['log_id'] = log_id
        context['current_frame'] = current_frame
        # we have to get the frames for top and bottom image and then remove the duplicates here, because sometime we have only one image in the 
        # first frame
        frames = FrameFilter.objects.filter(
            log_id=log_id,
            user=self.request.user,
        ).first()
        if frames:
            context['frame_numbers'] = Image.objects.filter(log_id=log_id, frame_number__in=frames.frames["frame_list"]).order_by('frame_number').values_list('frame_number', flat=True).distinct()
        else:
            context['frame_numbers'] = Image.objects.filter(log_id=log_id).order_by('frame_number').values_list('frame_number', flat=True).distinct()
        current_index = list(context['frame_numbers']).index(current_frame)
        context['prev_frame'] = list(context['frame_numbers'])[current_index - 1] if current_index > 0 else None
        context['next_frame'] = list(context['frame_numbers'])[current_index + 1] if current_index < len(context['frame_numbers']) - 1 else None
        # handle the case that we do have a bottom image in the frame
        if context['bottom_image']:
            # update the image url
            # TODO: dynamically add the url based on which server is online
            context['bottom_image'].image_url = "https://logs.berlin-united.com/" + context['bottom_image'].image_url

            bottom_annotation = Annotation.objects.filter(image=context['bottom_image'].id).values_list('annotation', flat=True).first()
            if bottom_annotation:
                context['bottom_annotation'] = json.dumps(bottom_annotation) 
            else:
                # add empty annotations when we could not load annotations
                context['bottom_annotation'] = json.dumps({}) 
        else:
            # add a dummy image if we don't have an image from the database
            context['bottom_image'] = None
            #context['bottom_image'] = Image()
            #context['bottom_image'].image_url = "https://dummyimage.com/640x4:3/"
            #context['bottom_image'].id = -1

            # add empty annotations when we don't have an image
            context['bottom_annotation'] = json.dumps({})
        
        # handle the case that we do have a top image in the frame
        if context['top_image']:
            print("id:", context['top_image'].id)
            # update the image url
            # TODO: dynamically add the url based on which server is online
            context['top_image'].image_url = "https://logs.berlin-united.com/" + context['top_image'].image_url

            top_annotation = Annotation.objects.filter(image=context['top_image'].id).values_list('annotation', flat=True).first()
            if top_annotation:
                context['top_annotation'] = json.dumps(top_annotation) 
            else:
                # add empty annotations when we could not load annotations
                context['top_annotation'] = json.dumps({}) 
        else:
            print("set top image to none")
            # add a dummy image if we don't have an image from the database
            context['top_image'] = None
            #context['top_image'] = Image()
            #context['top_image'].image_url = "https://dummyimage.com/640x4:3/"
            #context['top_image'].id = -1

            # add empty annotations when we don't have an image
            context['top_annotation'] = json.dumps({})
        return render(request, 'frontend/image_detail.html', context)

    def patch(self, request, **kwargs):
        try:
            json_data = json.loads(request.body)
            print(json_data)
            my_image = Image.objects.get(id=int(json_data["image"]))

            annotation_instance, created = Annotation.objects.get_or_create(
                image=my_image,
                defaults={"annotation": json_data.get("annotations", {})},
            )

            if not created:
                annotation_instance.annotation = json_data.get("annotations", {})
                annotation_instance.save()


            return JsonResponse({"message": "Canvas data received and processed."})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

@method_decorator(login_required(login_url='mylogin'), name='dispatch')
class MultiView(View):
    def get_first_standby_frame(self, log_id):
        """
        response = client.behavior_frame_option.filter(
            log_id=168,
            option_name="decide_game_state",
            state_name="standby",
        )
        print(response)
        """
        behavior_data_combined =  BehaviorFrameOption.objects.select_related(
                'options_id',         # Joins BehaviorOption
                'active_state',       # Joins BehaviorOptionState
                'active_state__option_id'  # Joins BehaviorOption via BehaviorOptionState
            )
        behavior_frame_options = behavior_data_combined.filter(log_id=log_id, options_id__option_name="decide_game_state", active_state__name="standby").order_by('frame').first()
        return behavior_frame_options.frame

    def get(self, request, **kwargs):
        context = {}
        game_id = self.kwargs.get('pk')
        context["game_id"]= game_id

        current_frame = self.kwargs.get('frame')
        # we need to handle the generic foreign key here, we only want logs of type game
        logs = Log.objects.filter(object_id=game_id, content_type=ContentType.objects.get_for_model(Game)).order_by('id')
        top_images = list()
        frame_numbers = list()
        for idx, log in enumerate(logs):
            # TODO handle the logic that no image is present for the given frames
            """
            get all the frames for all logs
            slice them so they start at the same time
            have a default image in case no image is present for the frame

            potentially remove frames where no robot has any images
            potentially show the time
            """
            frame_number_list = Image.objects.filter(log_id=log.id, camera="TOP").order_by('frame_number').values_list('frame_number', flat=True).distinct()
            first_standby_frame = self.get_first_standby_frame(log.id)
            first_frame_index = list(frame_number_list).index(first_standby_frame)
            frame_number_list = list(frame_number_list)[first_frame_index:]
            frame_numbers.append(frame_number_list)
            a = Image.objects.filter(log_id=log.id, camera="TOP", frame_number=frame_number_list[current_frame]).first()
            
            print(frame_number_list)
            
            a.image_url = "https://logs.berlin-united.com/" + a.image_url
            top_images.append(a)
            print(a)


        # FIXME add prev and next frame here
        context['frame_numbers'] = range(len(frame_numbers[0]))
        context['current_frame'] = current_frame
        context['top_images'] = top_images
        context['next_frame'] = current_frame + 1
        return render(request, 'frontend/multiview.html', context)