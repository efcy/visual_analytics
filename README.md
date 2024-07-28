# Berlin United Visual Analytics Tool
The goal of of this tool is to make it possible to quickly view, annotate and analyze all of our RoboCup data. This tool is inspired by V7Labs Darwin Tool but we will also add a lot of other features to it as well.
Access to the V7 tool for inspiration can be given on request.

## Dev Setup
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
You can use different names for the database, user and password. But you have to export them as environment variables in your .bashrc. For example like this
```bash
export VAT_POSTGRES_DB=vat_test
export VAT_POSTGRES_USER=testuser
export VAT_POSTGRES_PASS=password
export VAT_POSTGRES_HOST=localhost
export VAT_POSTGRES_PORT=5432
```



## SDK
Our SDK will be published to pypi: https://pypi.org/project/BU-VAT/

### Old
Labelstudio Implementation for RoboCup SPL Data

start backend and frontend locally:
```bash
python manage.py runserver
```


```

Now roughly following: https://www.youtube.com/watch?v=c-QsfbznSXI&t=1s
- this uses jwt instead of token based auth -> see where problems might be later on

created the web folder like this:
npm create vite@latest web -- --template react

installed node with whatever version ubuntu 22.04 could install 

testing frontend with
npm run dev


Notes:
- all the routes should be viewable by logged in users, maybe?
    - not sure how we can restrict it to more fine grained selection of users