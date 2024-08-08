#!/bin/bash

# Check if $1 is provided
if [ -z "$1" ]; then
  echo "Error: No mode specified."
  echo "Usage: $0 {del|renew|create}"
  exit 1
fi

cd /tmp
# Set the mode based on $1
mode=$1

if [ "$mode" == "del" ]; then
  # Execute the drop database command
    sudo -u postgres psql -c "DROP DATABASE IF EXISTS vat_test";

    # Check if the command was successful
    if [ $? -eq 0 ]; then
        echo "Database vat_test deleted successfully."
        exit 0
    else
        echo "Failed to delete database vat_test."
        exit 1
    fi

elif [ "$mode" == "renew" ]; then
      # create db and user

    sudo -u postgres psql -c "CREATE DATABASE vat_test;"
    #fails if user is already created

    # set permissions
    sudo -u postgres psql -c  "GRANT ALL ON DATABASE vat_test TO testuser;"
    sudo -u postgres psql -c  "GRANT ALL PRIVILEGES ON DATABASE vat_test TO testuser;"
    sudo -u postgres psql -c  "ALTER DATABASE vat_test OWNER TO testuser;"
    sudo -u postgres psql -c  "GRANT ALL ON SCHEMA PUBLIC TO testuser;"


    # Check if the command was successful
    if [ $? -eq 0 ]; then
        echo "Database renewed successfully."
    else
        echo "Failed to renew database."
    fi

elif [ "$mode" == "create" ]; then
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
        echo "Database created successfully."
    else
        echo "Failed to create database."
    fi
    

else
  echo "Error: Invalid mode specified."
  echo "Usage: $0 {del|renew|create}"
  exit 1
fi

