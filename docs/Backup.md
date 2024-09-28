# Backups
You can create backups manually of the database that django is using by running
```bash
python manage.py dbbackup
```

The location is controlled by the env var VAT_BACKUP_FOLDER.
In k8s you have to run this command inside the backend pod

## Backup Automation
Can be done like this: 
https://django-cron.readthedocs.io/en/latest/installation.html
https://django-dbbackup.readthedocs.io/en/stable/integration.html

this still requires the operating systems crontab. Maybe using something like this: https://www.youtube.com/watch?v=tXwcTg43uxc
is better