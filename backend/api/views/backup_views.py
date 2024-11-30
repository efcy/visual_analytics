from django.http import JsonResponse
from ..models import *
import json
from pathlib import Path
from django.core.serializers.json import DjangoJSONEncoder
from datetime import datetime, date

def serialize_django_object(obj):
    """Helper function to serialize Django models to dicts."""
    if obj is None:
        return None
    return {
        field.name: getattr(obj, field.name)
        for field in obj._meta.fields
    }


class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (datetime, date)):
            return obj.isoformat()
        return super().default(obj)


def backup(request, id):
        # Simulate some action (replace this with actual code)
        if Log.objects.filter(id=id).exists():
            
            log_id = id
            output_file = f'{id}.json'

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
                    'event': serialize_django_object(log.game_id.event_id),
                    'game': serialize_django_object(log.game_id),
                    'log': serialize_django_object(log),
                    'log_status': serialize_django_object(log.log_status) if hasattr(log, 'log_status') else None,
                    'images': [serialize_django_object(img) for img in log.images.all()],
                    'annotations': [
                        serialize_django_object(img.Annotation) 
                        for img in log.images.all() 
                        if hasattr(img, 'Annotation')
                    ],
                    'cognition_representations': [
                        serialize_django_object(repr) 
                        for repr in log.cognition_repr.all()
                    ],
                    'motion_representations': [
                        serialize_django_object(repr) 
                        for repr in log.motion_repr.all()
                    ],
                    'behavior_options': [
                        serialize_django_object(opt) 
                        for opt in log.behavior_options.all()
                    ],
                    'behavior_option_states': [
                        serialize_django_object(state)
                        for option in log.behavior_options.all()
                        for state in option.behavior_options_states.all()
                    ],
                    'behavior_frame_options': [
                        serialize_django_object(frame_opt) 
                        for frame_opt in log.behavior_frame_option.all()
                    ],
                    'xabsl_symbol_complete': (
                        serialize_django_object(log.xabsl_symbol_complete) 
                        if hasattr(log, 'xabsl_symbol_complete') else None
                    ),
                    'xabsl_symbol_sparse': [
                        serialize_django_object(symbol) 
                        for symbol in log.xabsl_symbol_sparse.all()
                    ],
                    'frame_filters': [
                        serialize_django_object(filter) 
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

                    result = {"success": True, "message": f"Backup for ID {id} executed."}

                    return JsonResponse(result)
            except Exception as e:
              return JsonResponse({"error": "error"}, status=503)
                
            
       
        else:
            return JsonResponse({"error": "Log does not exist"}, status=404)