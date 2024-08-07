#!/bin/bash

cd /tmp
# create db and user

sudo -u postgres psql -c "CREATE DATABASE vat_test;"
#fails if user is already created
sudo -u postgres psql -c "CREATE USER testuser WITH PASSWORD 'password';"

# set permissions
sudo -u postgres psql -c  "GRANT ALL ON DATABASE vat_test TO testuser;"
sudo -u postgres psql -c  "GRANT ALL PRIVILEGES ON DATABASE vat_test TO testuser;"
sudo -u postgres psql -c  "ALTER DATABASE vat_test OWNER TO testuser;"
sudo -u postgres psql -c  "GRANT ALL ON SCHEMA PUBLIC TO testuser;"


# Check if the command was successful
if [ $? -eq 0 ]; then
    echo "Database $1 renewed successfully."
else
    echo "Failed to renew database $1."
fi
