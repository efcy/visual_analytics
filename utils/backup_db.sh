#!/bin/bash
# kubectl port-forward postgres-postgresql-0 -n postgres 1234:5432

# Database connection details
DB_HOST="localhost"
DB_PORT="1234"
DB_USER="naoth"
DB_NAME="vat"


mkdir -p sql_output

# this would only export the schema but also everything from django as well
#pg_dump -h localhost -p 1234 -U naoth -d vat -s > schema.sql

# export all small tables in one go
pg_dump -h $DB_HOST -p $DB_PORT -U $DB_USER -d $DB_NAME -t api_event --data-only > sql_output/events.sql
pg_dump -h $DB_HOST -p $DB_PORT -U $DB_USER -d $DB_NAME -t api_game --data-only > sql_output/game.sql
pg_dump -h $DB_HOST -p $DB_PORT -U $DB_USER -d $DB_NAME -t api_log --data-only > sql_output/log.sql
pg_dump -h $DB_HOST -p $DB_PORT -U $DB_USER -d $DB_NAME -t api_logstatus --data-only > sql_output/logstatus.sql
pg_dump -h $DB_HOST -p $DB_PORT -U $DB_USER -d $DB_NAME -t api_xabslsymbolcomplete --data-only > sql_output/xabslsymbolcomplete.sql

# Fetch all distinct log id values
LOG_IDS=($(psql -h $DB_HOST -p $DB_PORT -U $DB_USER -d $DB_NAME -t -c "SELECT DISTINCT id FROM api_log;"))
LOG_IDS=(168)
# TODO what about "api_annotation" 
TABLE_NAMES=("api_behaviorframeoption" "api_behavioroption" "api_behavioroptionstate" "api_cognitionrepresentation" "api_motionrepresentation" "api_xabslsymbolsparse" api_image)

# Loop through each log_id_id
for LOG_ID in "${LOG_IDS[@]}"; do
    echo "Exporting data for log_id_id = $LOG_ID..."
    for TABLE_NAME in "${TABLE_NAMES[@]}"; do
        echo -e "\tExporting data for table = $TABLE_NAME ..."
        temp_table_name=(temp_${table})

        # Create a temporary table for the current log_id_id
        psql -h $DB_HOST -p $DB_PORT -U $DB_USER -d $DB_NAME -c "
            CREATE TABLE $temp_table_name AS
            SELECT * FROM $TABLE_NAME WHERE log_id_id = $LOG_ID;
        "
        # Dump the temporary table to a file
        pg_dump -h $DB_HOST -p $DB_PORT -U $DB_USER -d $DB_NAME -t $temp_table_name --data-only > sql_output/${TABLE_NAME}_${LOG_ID}.sql

        # Drop the temporary table
        psql -h $DB_HOST -p $DB_PORT -U $DB_USER -d $DB_NAME -c "
            DROP TABLE $temp_table_name;
        "
        echo -e "\tExported data for log_id_id = $LOG_ID to ${TABLE_NAME}_${LOG_ID}.sql"
    done
done
