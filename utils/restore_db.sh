# Database connection details
DB_HOST="localhost"
DB_PORT="5432"
DB_USER="naoth"
DB_NAME="restore_test"

# we need to connect to an existing database somehow - fix this for the case that nothing exists
psql -h $DB_HOST -p $DB_PORT -U $DB_USER -d vat -c "DROP DATABASE IF EXISTS $DB_NAME";
psql -h $DB_HOST -p $DB_PORT -U $DB_USER -d vat -c "CREATE DATABASE $DB_NAME;"

# TODO run python manage.py migrate here with the existing migration files - this will create the schemas for all tables

psql -q -h $DB_HOST -p $DB_PORT -U $DB_USER -d $DB_NAME -f "sql_output/events.sql"
psql -q -h $DB_HOST -p $DB_PORT -U $DB_USER -d $DB_NAME -f "sql_output/game.sql"
psql -q -h $DB_HOST -p $DB_PORT -U $DB_USER -d $DB_NAME -f "sql_output/log.sql"
psql -q -h $DB_HOST -p $DB_PORT -U $DB_USER -d $DB_NAME -f "sql_output/logstatus.sql"
psql -q -h $DB_HOST -p $DB_PORT -U $DB_USER -d $DB_NAME -f "sql_output/xabslsymbolcomplete.sql"


# patch sql exports (TODO: do this in a loop for all sql files)
sed -i 's/temp_/api_behavioroption/g' sql_output/api_behavioroption_1.sql
sed -i 's/temp_/api_behavioroption/g' sql_output/api_behavioroption_2.sql
sed -i 's/temp_/api_behavioroption/g' sql_output/api_behavioroption_168.sql

sed -i 's/temp_/api_behavioroptionstate/g' sql_output/api_behavioroptionstate_1.sql
sed -i 's/temp_/api_behavioroptionstate/g' sql_output/api_behavioroptionstate_2.sql
sed -i 's/temp_/api_behavioroptionstate/g' sql_output/api_behavioroptionstate_168.sql

sed -i 's/temp_/api_behaviorframeoption/g' sql_output/api_behaviorframeoption_1.sql
sed -i 's/temp_/api_behaviorframeoption/g' sql_output/api_behaviorframeoption_2.sql
sed -i 's/temp_/api_behaviorframeoption/g' sql_output/api_behaviorframeoption_168.sql

sed -i 's/temp_/api_xabslsymbolsparse/g' sql_output/api_xabslsymbolsparse_1.sql
sed -i 's/temp_/api_xabslsymbolsparse/g' sql_output/api_xabslsymbolsparse_2.sql
sed -i 's/temp_/api_xabslsymbolsparse/g' sql_output/api_xabslsymbolsparse_168.sql

sed -i 's/temp_/api_cognitionrepresentation/g' sql_output/api_cognitionrepresentation_1.sql
sed -i 's/temp_/api_cognitionrepresentation/g' sql_output/api_cognitionrepresentation_2.sql
sed -i 's/temp_/api_cognitionrepresentation/g' sql_output/api_cognitionrepresentation_168.sql

sed -i 's/temp_/api_motionrepresentation/g' sql_output/api_motionrepresentation_1.sql
sed -i 's/temp_/api_motionrepresentation/g' sql_output/api_motionrepresentation_2.sql
sed -i 's/temp_/api_motionrepresentation/g' sql_output/api_motionrepresentation_168.sql

sed -i 's/temp_/api_image/g' sql_output/api_image_1.sql
sed -i 's/temp_/api_image/g' sql_output/api_image_2.sql
sed -i 's/temp_/api_image/g' sql_output/api_image_168.sql

# restore the data
psql -h $DB_HOST -p $DB_PORT -U $DB_USER -d $DB_NAME -f "sql_output/api_behavioroption_1.sql"
psql -h $DB_HOST -p $DB_PORT -U $DB_USER -d $DB_NAME -f "sql_output/api_behavioroption_2.sql"
psql -h $DB_HOST -p $DB_PORT -U $DB_USER -d $DB_NAME -f "sql_output/api_behavioroption_168.sql"

psql -h $DB_HOST -p $DB_PORT -U $DB_USER -d $DB_NAME -f "sql_output/api_behavioroptionstate_1.sql"
psql -h $DB_HOST -p $DB_PORT -U $DB_USER -d $DB_NAME -f "sql_output/api_behavioroptionstate_2.sql"
psql -h $DB_HOST -p $DB_PORT -U $DB_USER -d $DB_NAME -f "sql_output/api_behavioroptionstate_168.sql"

psql -h $DB_HOST -p $DB_PORT -U $DB_USER -d $DB_NAME -f "sql_output/api_behaviorframeoption_1.sql"
psql -h $DB_HOST -p $DB_PORT -U $DB_USER -d $DB_NAME -f "sql_output/api_behaviorframeoption_2.sql"
psql -h $DB_HOST -p $DB_PORT -U $DB_USER -d $DB_NAME -f "sql_output/api_behaviorframeoption_168.sql"

psql -h $DB_HOST -p $DB_PORT -U $DB_USER -d $DB_NAME -f "sql_output/api_xabslsymbolsparse_1.sql"
psql -h $DB_HOST -p $DB_PORT -U $DB_USER -d $DB_NAME -f "sql_output/api_xabslsymbolsparse_2.sql"
psql -h $DB_HOST -p $DB_PORT -U $DB_USER -d $DB_NAME -f "sql_output/api_xabslsymbolsparse_168.sql"

psql -h $DB_HOST -p $DB_PORT -U $DB_USER -d $DB_NAME -f "sql_output/api_cognitionrepresentation_1.sql"
psql -h $DB_HOST -p $DB_PORT -U $DB_USER -d $DB_NAME -f "sql_output/api_cognitionrepresentation_2.sql"
psql -h $DB_HOST -p $DB_PORT -U $DB_USER -d $DB_NAME -f "sql_output/api_cognitionrepresentation_168.sql"

psql -h $DB_HOST -p $DB_PORT -U $DB_USER -d $DB_NAME -f "sql_output/api_motionrepresentation_1.sql"
psql -h $DB_HOST -p $DB_PORT -U $DB_USER -d $DB_NAME -f "sql_output/api_motionrepresentation_2.sql"
psql -h $DB_HOST -p $DB_PORT -U $DB_USER -d $DB_NAME -f "sql_output/api_motionrepresentation_168.sql"

psql -h $DB_HOST -p $DB_PORT -U $DB_USER -d $DB_NAME -f "sql_output/api_image_168.sql"