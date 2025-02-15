# Backups
Database backups can be multiple hundreds of gigabyte. Tools like `python manage.py dbbackup` create one large backup file. This is not useful in our case. We wrote a custom python script that exports an sql file per log_id for every model that is dependent on the log model. That way each sql output file has manageable size.

## Create Backups
To export all data you can run:
```bash
python utils/backup.py -a -g -o <my_output_path>
```
If you want to run this locally or directly on the server and not inside a k8s pod you have to first setup port forwarding to the postgres port inside the postgres pod.
```bash
kubectl port-forward postgres-postgresql-0 -n postgres 1234:5432
```

The backup will only backup VAT data and now user related data.


## Restore a backup
Make sure you have a database where no data exists that is the same as the data you want to restore. In the backend folder run
```
python manage.py makemigrations
python mange.py migrate
python restore.py
```

If you deleted the whole database you need to setup user and organisations again manually.

## Backup Automation
Not implemented yet