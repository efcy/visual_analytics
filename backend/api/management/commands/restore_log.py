from django.core.management.base import BaseCommand
from django.db import transaction
import json
import gzip,time
from pathlib import Path
from datetime import datetime
from ...models import (
    Event, Game, Log, LogStatus, Image, Annotation, 
    CognitionRepresentation, MotionRepresentation, 
    BehaviorOption, BehaviorOptionState, 
    BehaviorFrameOption, XabslSymbolComplete, 
    XabslSymbolSparse
)

class Command(BaseCommand):
    help = 'Restores a log and all related data from a JSON export'

    def add_arguments(self, parser):
        parser.add_argument('input_file', type=str, help='Path to the JSON file to restore')

    def parse_datetime(self, datetime_str):
        """Parse datetime string to datetime object"""
        if not datetime_str:
            return None
        try:
            return datetime.fromisoformat(datetime_str)
        except ValueError:
            return None

    @transaction.atomic
    def handle(self, *args, **options):
        input_file = options['input_file']

        try:
            start_time = time.time()
            # Read the JSON file
            with gzip.open(input_file, 'rt') as f:
                export_data = json.load(f)

            print(f"file reading{time.time() - start_time}")
            # Restore Event
            event_data = export_data.get('event', {})
            event_id = event_data.pop('id', None)
            event, created = Event.objects.update_or_create(
                id=event_id,
                defaults=event_data
            )

            # Restore Game
            game_data = export_data.get('game', {})
            game_data['event_id'] = event
            game_id = game_data.pop('id', None)
            game, created = Game.objects.update_or_create(
                id=game_id,
                defaults=game_data
            )

            # Restore Log
            log_data = export_data.get('log', {})
            log_data['game_id'] = game
            log_id = log_data.pop('id', None)
            log, created = Log.objects.update_or_create(
                id=log_id,
                defaults=log_data
            )
            
            # Restore LogStatus
            log_status_data = export_data.get('log_status', {})
            if log_status_data:
                log_status_data['log_id'] = log
                LogStatus.objects.update_or_create(
                    log_id=log,
                    defaults=log_status_data
                )

            # Restore Images
            images_data = export_data.get('images', [])
            images_to_create = []
            for img_data in images_data:
                img_data['log'] = log
                img_id = img_data.pop('id', None)
                img, created = Image.objects.update_or_create(
                    id=img_id,
                    defaults=img_data
                )
                # Restore Annotations (if exists)
                ann_data = next((ann for ann in export_data.get('annotations', []) 
                                 if ann.get('image') == img_id), None)
                if ann_data:
                    Annotation.objects.update_or_create(
                        image=img,
                        defaults=ann_data
                    )
            print(f"image {time.time() - start_time}")
            

                        # Restore Cognition Representations
            cog_repr_data = export_data.get('cognition_representations', [])

            # Collect cognition representations for bulk update
            cog_reprs_to_create = []
            for repr_data in cog_repr_data:
                repr_data['log_id'] = log
                repr_id = repr_data.pop('id', None)
                
                cog_repr = CognitionRepresentation(
                    id=repr_id,
                    **repr_data
                )
                cog_reprs_to_create.append(cog_repr)

            # Use bulk_create for improved performance
            CognitionRepresentation.objects.bulk_create(
            cog_reprs_to_create, 
            batch_size=1000  # Adjust batch size as needed
            )


            print(f"cognition {time.time() - start_time}")
            # Restore Motion Representations
            motion_repr_data = export_data.get('motion_representations', [])
            for repr_data in motion_repr_data:
                repr_data['log_id'] = log
                repr_id = repr_data.pop('id', None)
                MotionRepresentation.objects.update_or_create(
                    id=repr_id,
                    defaults=repr_data
                )
            print(f"motion {time.time() - start_time}")
            # Restore Behavior Options
            behavior_options_data = export_data.get('behavior_options', [])
            behavior_options = []
            for opt_data in behavior_options_data:
                opt_data['log_id'] = log
                opt_id = opt_data.pop('id', None)
                option, created = BehaviorOption.objects.update_or_create(
                    id=opt_id,
                    defaults=opt_data
                )
                behaviors_opt_states = export_data.get('behavior_option_states', [])
                # Restore Option States
                for state_data in behaviors_opt_states:
                    if state_data.get('option_id') == opt_id:
                        state_data['log_id'] = log
                        state_data['option_id'] = option
                        state_id = state_data.pop('id', None)
                        BehaviorOptionState.objects.update_or_create(
                            id=state_id,
                            defaults=state_data
                        )

            
            # Restore Xabsl Symbol Complete
            xabsl_symbol_complete_data = export_data.get('xabsl_symbol_complete', {})
            if xabsl_symbol_complete_data:
                xabsl_symbol_complete_data['log_id'] = log
                XabslSymbolComplete.objects.update_or_create(
                    log_id=log,
                    defaults=xabsl_symbol_complete_data
                )

            # Restore Xabsl Symbol Sparse
            xabsl_symbol_sparse_data = export_data.get('xabsl_symbol_sparse', [])
            for symbol_data in xabsl_symbol_sparse_data:
                symbol_data['log_id'] = log
                symbol_id = symbol_data.pop('id', None)
                XabslSymbolSparse.objects.update_or_create(
                    id=symbol_id,
                    defaults=symbol_data
                )
            print(f"xabsl {time.time() - start_time}")
             # Restore Behavior Frame Options
            behavior_frame_opts_data = export_data.get('behavior_frame_options', [])
            print(len(behavior_frame_opts_data))

            # Collect unique option and state IDs first
            unique_option_ids = set(frame_opt_data.get('options_id') for frame_opt_data in behavior_frame_opts_data)
            unique_state_ids = set(frame_opt_data.get('active_state') for frame_opt_data in behavior_frame_opts_data)

            # Bulk fetch options and states to reduce database queries
            options_map = {opt.id: opt for opt in BehaviorOption.objects.filter(id__in=unique_option_ids)}
            states_map = {state.id: state for state in BehaviorOptionState.objects.filter(id__in=unique_state_ids)}

            # Prepare frame options for bulk creation
            frame_options_to_create = []
            for frame_opt_data in behavior_frame_opts_data:
                frame_opt_id = frame_opt_data.pop('id', None)
                
                # Use the preloaded maps to avoid individual queries
                option = options_map.get(frame_opt_data.get('options_id'))
                active_state = states_map.get(frame_opt_data.get('active_state'))
                
                if not option or not active_state:
                    continue
                
                frame_opt_data['log_id'] = log
                frame_opt_data['options_id'] = option
                frame_opt_data['active_state'] = active_state
                
                frame_option = BehaviorFrameOption(
                    id=frame_opt_id,
                    **frame_opt_data
                )
                frame_options_to_create.append(frame_option)

            # Use bulk_create for improved performance
            BehaviorFrameOption.objects.bulk_create(
                frame_options_to_create, 
                batch_size=1000  # Adjust batch size based on your system's memory and database capabilities
            )

            print(f"be frame options {time.time() - start_time}")
        

            self.stdout.write(
                self.style.SUCCESS(f'Successfully restored log {log.id} from {input_file}')
            )

        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error during restoration: {str(e)}')
            )