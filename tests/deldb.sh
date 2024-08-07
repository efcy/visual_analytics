#!/bin/bash

cd /tmp
# Execute the drop database command
sudo -u postgres psql -c "DROP DATABASE IF EXISTS $1;"

# Check if the command was successful
if [ $? -eq 0 ]; then
    echo "Database $1 deleted successfully."
else
    echo "Failed to delete database $1."
fi



