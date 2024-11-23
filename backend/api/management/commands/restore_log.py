from django.core.management.base import BaseCommand
from ...models import (
    Log, LogStatus, Image, Annotation, CognitionRepresentation, 
    MotionRepresentation, BehaviorOption, BehaviorOptionState, 
    BehaviorFrameOption, XabslSymbolComplete, XabslSymbolSparse,
    FrameFilter, Game, Event
)
import json
from datetime import datetime
from django.contrib.auth import get_user_model
from pathlib import Path

User = get_user_model()

class Command(BaseCommand):
    help = 'Imports log data from a JSON export file'

    def add_arguments(self, parser):
        parser.add_argument(
            'input_file',
            type=str,
            help='Path to the JSON file containing the exported data'
        )
        parser.add_argument(
            '--user',
            type=int,
            help='User ID to associate with frame filters (required if frame filters exist)',
            required=False
        )

    def parse_datetime(self, dt_str):
        """Convert ISO format datetime string back to datetime object"""
        if not dt_str:
            return None
        try:
            return datetime.fromisoformat(dt_str)
        except (ValueError, TypeError):
            return None

    def clean_data(self, data):
        """Remove None values and convert datetime strings"""
        if not data:
            return {}
        
        cleaned = {}
        for key, value in data.items():
            if value is not None:
                if isinstance(value, str) and (
                    'time' in key.lower() or 
                    'date' in key.lower() or 
                    key in ['created', 'modified']
                ):
                    cleaned[key] = self.parse_datetime(value)
                else:
                    cleaned[key] = value
        return cleaned

    def handle(self, *args, **options):
        input_file = options['input_file']
        user_id = options.get('user')

        if not Path(input_file).exists():
            self.stdout.write(
                self.style.ERROR(f'Input file {input_file} does not exist')
            )
            return

        try:
            with open(input_file, 'r') as f:
                data = json.load(f)

            # Create objects in the correct order to maintain relationships
            
            # 1. Event
            event_data = self.clean_data(data.get('event'))
            event_id = event_data.pop('id')
            event, _ = Event.objects.get_or_create(
                id=event_id,
                defaults=event_data
            )
            self.stdout.write(self.style.SUCCESS(f'Imported Event: {event}'))

            # 2. Game
            game_data = self.clean_data(data.get('game'))
            game_id = game_data.pop('id')
            game_data['event_id'] = event
            game, _ = Game.objects.get_or_create(
                id=game_id,
                defaults=game_data
            )
            self.stdout.write(self.style.SUCCESS(f'Imported Game: {game}'))

            # 3. Log
            log_data = self.clean_data(data.get('log'))
            log_id = log_data.pop('id')
            log_data['game_id'] = game
            log, _ = Log.objects.get_or_create(
                id=log_id,
                defaults=log_data
            )
            self.stdout.write(self.style.SUCCESS(f'Imported Log: {log}'))

            # 4. LogStatus
            if 'log_status' in data:
                log_status_data = self.clean_data(data['log_status'])
                LogStatus.objects.get_or_create(
                    log_id=log,
                    defaults={k: v for k, v in log_status_data.items() if k != 'log_id'}
                )
                self.stdout.write(self.style.SUCCESS('Imported LogStatus'))

            # 5. Images
            for img_data in data.get('images', []):
                img_data = self.clean_data(img_data)
                img_id = img_data.pop('id')
                img_data['log'] = log
                Image.objects.get_or_create(
                    id=img_id,
                    defaults=img_data
                )
            self.stdout.write(self.style.SUCCESS('Imported Images'))

            # 6. Annotations
            for ann_data in data.get('annotations', []):
                ann_data = self.clean_data(ann_data)
                image_id = ann_data.pop('image')
                try:
                    image = Image.objects.get(id=image_id)
                    Annotation.objects.get_or_create(
                        image=image,
                        defaults=ann_data
                    )
                except Image.DoesNotExist:
                    self.stdout.write(
                        self.style.WARNING(f'Image {image_id} not found for annotation')
                    )
            self.stdout.write(self.style.SUCCESS('Imported Annotations'))

            # 7. CognitionRepresentation
            for cogn_data in data.get('cognition_representations', []):
                cogn_data = self.clean_data(cogn_data)
                cogn_id = cogn_data.pop('id')
                cogn_data['log_id'] = log
                CognitionRepresentation.objects.get_or_create(
                    id=cogn_id,
                    defaults=cogn_data
                )
            self.stdout.write(self.style.SUCCESS('Imported CognitionRepresentations'))

            # 8. MotionRepresentation
            for motion_data in data.get('motion_representations', []):
                motion_data = self.clean_data(motion_data)
                motion_id = motion_data.pop('id')
                motion_data['log_id'] = log
                MotionRepresentation.objects.get_or_create(
                    id=motion_id,
                    defaults=motion_data
                )
            self.stdout.write(self.style.SUCCESS('Imported MotionRepresentations'))

            # 9. BehaviorOptions
            behavior_options_map = {}  # To store old_id -> new_object mapping
            for opt_data in data.get('behavior_options', []):
                opt_data = self.clean_data(opt_data)
                old_id = opt_data.pop('id')
                opt_data['log_id'] = log
                option, _ = BehaviorOption.objects.get_or_create(
                    log_id=log,
                    xabsl_internal_option_id=opt_data.get('xabsl_internal_option_id'),
                    defaults=opt_data
                )
                behavior_options_map[old_id] = option
            self.stdout.write(self.style.SUCCESS('Imported BehaviorOptions'))

            # 10. BehaviorOptionStates
            behavior_states_map = {}  # To store old_id -> new_object mapping
            for state_data in data.get('behavior_option_states', []):
                state_data = self.clean_data(state_data)
                old_id = state_data.pop('id')
                old_option_id = state_data.pop('option_id')
                state_data['option_id'] = behavior_options_map[old_option_id]
                state_data['log_id'] = log
                state, _ = BehaviorOptionState.objects.get_or_create(
                    log_id=log,
                    option_id=state_data['option_id'],
                    xabsl_internal_state_id=state_data.get('xabsl_internal_state_id'),
                    defaults=state_data
                )
                behavior_states_map[old_id] = state
            self.stdout.write(self.style.SUCCESS('Imported BehaviorOptionStates'))

            # 11. BehaviorFrameOption
            for frame_opt_data in data.get('behavior_frame_options', []):
                frame_opt_data = self.clean_data(frame_opt_data)
                old_options_id = frame_opt_data.pop('options_id')
                old_active_state = frame_opt_data.pop('active_state')
                frame_opt_data['log_id'] = log
                frame_opt_data['options_id'] = behavior_options_map[old_options_id]
                frame_opt_data['active_state'] = behavior_states_map[old_active_state]
                BehaviorFrameOption.objects.get_or_create(
                    log_id=log,
                    options_id=frame_opt_data['options_id'],
                    frame=frame_opt_data.get('frame'),
                    active_state=frame_opt_data['active_state'],
                    defaults=frame_opt_data
                )
            self.stdout.write(self.style.SUCCESS('Imported BehaviorFrameOptions'))

            # 12. XabslSymbolComplete
            if 'xabsl_symbol_complete' in data:
                symbol_complete_data = self.clean_data(data['xabsl_symbol_complete'])
                XabslSymbolComplete.objects.get_or_create(
                    log_id=log,
                    defaults={'data': symbol_complete_data.get('data')}
                )
            self.stdout.write(self.style.SUCCESS('Imported XabslSymbolComplete'))

            # 13. XabslSymbolSparse
            for symbol_data in data.get('xabsl_symbol_sparse', []):
                symbol_data = self.clean_data(symbol_data)
                symbol_data['log_id'] = log
                XabslSymbolSparse.objects.get_or_create(
                    log_id=log,
                    frame=symbol_data.get('frame'),
                    defaults=symbol_data
                )
            self.stdout.write(self.style.SUCCESS('Imported XabslSymbolSparse'))

            # 14. FrameFilter (only if user_id is provided)
            if user_id and 'frame_filters' in data:
                try:
                    user = User.objects.get(id=user_id)
                    for filter_data in data['frame_filters']:
                        filter_data = self.clean_data(filter_data)
                        filter_data['log_id'] = log
                        filter_data['user'] = user
                        FrameFilter.objects.get_or_create(
                            log_id=log,
                            user=user,
                            defaults=filter_data
                        )
                    self.stdout.write(self.style.SUCCESS('Imported FrameFilters'))
                except User.DoesNotExist:
                    self.stdout.write(
                        self.style.WARNING(f'User {user_id} not found, skipping frame filters')
                    )

            self.stdout.write(
                self.style.SUCCESS('Successfully imported all data')
            )

        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error during import: {str(e)}')
            )