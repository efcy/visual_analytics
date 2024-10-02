# Backups

## Create Backups

Locally you can create backups of the database that django is using by running
```bash
python manage.py dbbackup
```
The location is controlled by the env var `VAT_BACKUP_FOLDER`.

### K8s
In k8s you have to run this command inside the backend pod
```bash
k exec -it vat-backend-5b977bbf57-zqfqj -c backend -- python manage.py dbbackup
```

The backup file will be saved on the server where k8s is running on. You can download it from there.

## Restore a backup
You can use backups from the live version and use it in your local version. This only works if the postgres database is set up in the same way as the live version.
TODO: check if password also needs to be the same

```bash
python manage.py dbrestore -I <backup file>
```

## Backup Automation
Not implemented yet