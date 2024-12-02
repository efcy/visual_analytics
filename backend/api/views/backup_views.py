from django.http import JsonResponse
from ..models import *
import json
from pathlib import Path
from django.core.serializers.json import DjangoJSONEncoder
from datetime import datetime, date
from django.core import management
import threading,os

def backup(request, id):
        
        def run_backup(log_id):
            management.call_command('export_log',id,f'--output=./backups/{id}.json')
        
        thread = threading.Thread(target=run_backup, args=(id,))
        thread.start()
        return JsonResponse({"message":f"started backing up log with id={id}"}, status=200)

def backup_status(request,id):
        path = f"./backups/{id}.json"
        if os.path.exists(path):
            try:
                # Try to open the file in exclusive mode
                with open(path, 'a'):
                    return JsonResponse({"message":f"backup is done"})
            except IOError:
                return JsonResponse({"message":f"backup is still being written"})
        else:
            return JsonResponse({"message":f"backup is still being created"})