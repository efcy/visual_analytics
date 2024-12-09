from django.http import JsonResponse
from ..models import *
import json
from pathlib import Path
from django.core.serializers.json import DjangoJSONEncoder
from datetime import datetime, date
from django.core import management
import threading,os
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView

class backup(APIView):
    permission_classes = [IsAuthenticated]
    
    def run_backup(self,id):
        management.call_command('export_log',id,f'--output=./backups/{id}.json')
    
    def post(self,request,id):

        thread = threading.Thread(target=self.run_backup, args=(id,))
        thread.start()
        return JsonResponse({"message":f"started backing up log with id={id}"}, status=200)

class backup_status(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request,id):
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
