# Backups

## Create Backups

Locally you can create backups of the database that django is using by running
```bash
python manage.py dbbackup
```
The location is controlled by the env var `VAT_BACKUP_FOLDER`. 
It is advised to exclude the user tables from the backup. You can do it like this:

```bash
python manage.py dbbackup -x user_vatuser -x user_organization -x authtoken_token
```

More infoprmation can be found at: https://django-dbbackup.readthedocs.io/en/master/commands.html#dbrestore

### K8s
In k8s you have to run this command inside the backend pod
```bash
k exec -it vat-backend-5b977bbf57-zqfqj -c backend -- python manage.py dbbackup
```

The backup file will be saved on the server where k8s is running on. You can download it from there.

## Restore a backup
You can use backups from the live version and use it in your local version. This only works if the postgres database is set up in the same way as the live version.


```bash
python manage.py dbrestore -I <backup file>
```

### Troubleshooting
see this issue if you have errors while restoring the backup that have to do with constraints
https://github.com/jazzband/django-dbbackup/issues/478
pyt
## Backup Automation
Not implemented yet