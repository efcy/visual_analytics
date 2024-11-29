from django.core.management.base import BaseCommand
from django.db.models import Prefetch
from ...models import (
    Log, LogStatus, Image, Annotation, CognitionRepresentation, 
    MotionRepresentation, BehaviorOption, BehaviorOptionState, 
    BehaviorFrameOption, XabslSymbolComplete, XabslSymbolSparse,
    FrameFilter, Game, Event
)
import json
from pathlib import Path
from datetime import datetime, date
from django.forms.models import model_to_dict

class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (datetime, date)):
            return obj.isoformat()
        return super().default(obj)

class Command(BaseCommand):
    help = 'Exports a single log and all related data for development environments'

    def add_arguments(self, parser):
        parser.add_argument('log_id', type=int, help='ID of the log to export')
        parser.add_argument(
            '--output', 
            type=str, 
            default='dev_data.json',
            help='Output file path'
        )
    
    def serialize_django_object(self, obj):
        """Helper method to convert Django model instance to dict with proper datetime handling"""
        if obj is None:
            return None
        
        # Convert model instance to dictionary
        data = model_to_dict(obj)
        
        # Handle datetime and date objects
        for key, value in data.items():
            if isinstance(value, (datetime, date)):
                data[key] = value.isoformat()
        
        return data

    def handle(self, *args, **options):
        log_id = options['log_id']
        output_file = options['output']

        try:
            # Get the log with all related data
            log = Log.objects.select_related(
                'log_status',
                'game_id',
                'game_id__event_id',
                'xabsl_symbol_complete'
            ).prefetch_related(
                'images',
                'images__Annotation',
                'cognition_repr',
                'motion_repr',
                'behavior_options',
                'behavior_options__behavior_options_states',
                'behavior_frame_option',
                'xabsl_symbol_sparse',
                'frame_filter'
            ).get(id=log_id)

            # Prepare the data structure with custom serialization
            export_data = {
                'event': self.serialize_django_object(log.game_id.event_id),
                'game': self.serialize_django_object(log.game_id),
                'log': self.serialize_django_object(log),
                'log_status': self.serialize_django_object(log.log_status) if hasattr(log, 'log_status') else None,
                'images': [self.serialize_django_object(img) for img in log.images.all()],
                'annotations': [
                    self.serialize_django_object(img.Annotation) 
                    for img in log.images.all() 
                    if hasattr(img, 'Annotation')
                ],
                'cognition_representations': [
                    self.serialize_django_object(repr) 
                    for repr in log.cognition_repr.all()
                ],
                'motion_representations': [
                    self.serialize_django_object(repr) 
                    for repr in log.motion_repr.all()
                ],
                'behavior_options': [
                    self.serialize_django_object(opt) 
                    for opt in log.behavior_options.all()
                ],
                'behavior_option_states': [
                    self.serialize_django_object(state)
                    for option in log.behavior_options.all()
                    for state in option.behavior_options_states.all()
                ],
                'behavior_frame_options': [
                    self.serialize_django_object(frame_opt) 
                    for frame_opt in log.behavior_frame_option.all()
                ],
                'xabsl_symbol_complete': (
                    self.serialize_django_object(log.xabsl_symbol_complete) 
                    if hasattr(log, 'xabsl_symbol_complete') else None
                ),
                'xabsl_symbol_sparse': [
                    self.serialize_django_object(symbol) 
                    for symbol in log.xabsl_symbol_sparse.all()
                ],
                'frame_filters': [
                    self.serialize_django_object(filter) 
                    for filter in log.frame_filter.all()
                ],
            }
            print(f"Images length: {len(log.images.all())}")
            print(f"Annotations length: {len([img.Annotation for img in log.images.all() if hasattr(img, 'Annotation')])}")
            print(f"Cognition representations length: {len(log.cognition_repr.all())}")
            print(f"Motion representations length: {len(log.motion_repr.all())}")
            print(f"Behavior options length: {len(log.behavior_options.all())}")
            print(f"Behavior option states length: {len([state for option in log.behavior_options.all() for state in option.behavior_options_states.all()])}")
            print(f"Behavior frame options length: {len(log.behavior_frame_option.all())}")
            print(f"XABSL symbol sparse length: {len(log.xabsl_symbol_sparse.all())}")
            print(f"Frame filters length: {len(log.frame_filter.all())}")
                        # Remove None values
            export_data = {k: v for k, v in export_data.items() if v is not None}

            # Ensure the output directory exists
            Path(output_file).parent.mkdir(parents=True, exist_ok=True)

            # Write to file using custom encoder
            with open(output_file, 'w') as f:
                json.dump(
                    export_data,
                    f,
                    indent=2,
                    cls=DateTimeEncoder
                )

            self.stdout.write(
                self.style.SUCCESS(f'Successfully exported log {log_id} to {output_file}')
            )

        except Log.DoesNotExist:
            self.stdout.write(
                self.style.ERROR(f'Log with id {log_id} does not exist')
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error during export: {str(e)}')
            )