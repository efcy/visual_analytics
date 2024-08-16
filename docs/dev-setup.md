# Dev Setup

## Setup Postgres
Install postgres in your ubuntu or ubuntu wsl machine:
```bash
sudo apt install postgresql postgresql-contrib
```
Change this line in `/etc/postgresql/16/main/pg_hba.conf`
```txt
local   all             all                                     peer
```
to
```txt
local   all             all                                     md5
```

log into postgres and setup a new user with sufficient permissions
```bash
sudo -u postgres psql

CREATE DATABASE vat_test;
CREATE USER testuser WITH PASSWORD 'password';

# set permissions
GRANT ALL ON DATABASE vat_test TO testuser;
GRANT ALL PRIVILEGES ON DATABASE vat_test TO testuser;
ALTER DATABASE vat_test OWNER TO testuser;
GRANT ALL ON SCHEMA PUBLIC TO testuser;
```

you can also use the dbutils.sh in /utils to create the test database with the default values stated below.

```bash
./dbutils.sh create
```

You can use different names for the database, user and password. But you have to export them as environment variables in your .bashrc. For example like this
```bash
export VAT_POSTGRES_DB=vat_test
export VAT_POSTGRES_USER=testuser
export VAT_POSTGRES_PASS=password
export VAT_POSTGRES_HOST=localhost
export VAT_POSTGRES_PORT=5432
```

## Setup Django
Create local user for you django

```bash
python manage.py createsuperuser
```

## Setup Node.js
We currently use node.js 18.
```bash
curl -fsSL https://deb.nodesource.com/setup_18.x -o nodesource_setup.sh
sudo -E bash nodesource_setup.sh
sudo apt-get install -y nodejs
```

In the web folder run:
```bash
npm install
npm run dev
```

## Install sdk locally
In the repo folder install the sdk with
```bash
python -m pip install -e sdk
```
then log in to django admin page on http://localhost:8000/admin/ and get the API Token for use with the sdk. If you plan to use the predefined functions for inserting data you need to expose the API Key as an environment variable:
```bash
export VAT_API_TOKEN=<your api token>
```

## Add Data
Make sure you have the log folder mounted via sshfs. 
```bash
export VAT_LOG_ROOT=<path to folder containing all the events>
```