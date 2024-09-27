This folder contains several utility scripts


### dbutils.sh
used to setup the database or renew it and delete all migration files
useful when encountering errors after model changes

usage:
```bash
./dbutils.sh renew|create
```

### input_data.py
This script parses NaoTH Logs from specified events and inputs them in the database using the sdk

Setup
```bash
export VAT_API_URL = "Adress of django server"
export VAT_LOG_ROOT = "Path of naothlog root folder"
export VAT_API_TOKEN = "your api token"
```

### input_images
insert img urls for existing robot data 

Setup
```bash
export VAT_API_URL = "Adress of django server"
export VAT_LOG_ROOT = "Path of naothlog root folder"
export VAT_API_TOKEN = "your api token"
```
