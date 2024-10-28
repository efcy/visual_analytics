# Setup Postgres
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

CREATE DATABASE vat;
CREATE USER testuser WITH PASSWORD 'password';

# set permissions
GRANT ALL ON DATABASE vat TO naoth;
GRANT ALL PRIVILEGES ON DATABASE vat TO naoth;
ALTER DATABASE vat OWNER TO naoth;
GRANT ALL ON SCHEMA PUBLIC TO naoth;
```

you can also use the dbutils.sh in /utils to create the test database using the enviroment variables below

```bash
./dbutils.sh create
```


For django and the utility scripts to work you need to set these enviroment variables by adding it to your .bashrc file

```bash
export VAT_POSTGRES_DB=vat
export VAT_POSTGRES_USER=naoth
export VAT_POSTGRES_PASS=password
export VAT_POSTGRES_HOST=localhost
export VAT_POSTGRES_PORT=5432
```

NOTE: backups won't work with diffrent user or db names

