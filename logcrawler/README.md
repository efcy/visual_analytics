# Logcrawler
Scripts for inserting log data into the database. These scripts generally only need to be run once. 

The logcrawler scripts use the [VAAPI pip package](https://pypi.org/project/vaapi/) to communicate with the backend.

You will need these environment variables in order to run the scripts:
```bash
VAT_LOG_ROOT=<"path to folder containing all the events">
VAT_API_URL=<"http://127.0.0.1:8000/ or https://api.berlin-united.com/">
VAT_API_TOKEN=<token you can get from the website>
```

## Access the log folder
If you have a large disk you can download the log folders in the correct structure to your disk and use the logs locally. This is recommended if you want to add a whole event to the database.

TODO: write scripts that downloads all necessary files

Alternatively you can use sshfs. This is much slower then using local files.

TODO add sshfs tutorial here