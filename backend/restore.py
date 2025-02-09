import argparse
from pathlib import Path
import subprocess
import os
import psycopg2
from psycopg2 import sql
import time
from django.core import management

DB_HOST=os.getenv('VAT_POSTGRES_HOST')
DB_PORT=os.getenv('VAT_POSTGRES_PORT')
DB_USER=os.getenv('VAT_POSTGRES_USER')
DB_NAME=os.getenv('VAT_POSTGRES_DB')

def import_global_tables():
    sql_table = [
        "api_event.sql",
        "api_game.sql",
        "api_log.sql",
        "api_logstatus.sql",
        "api_xabslsymbolcomplete.sql",
        "api_annotation.sql"
    ]

    for file in sql_table:
        try:
            command = f"psql -h {DB_HOST} -p {DB_PORT} -U {DB_USER} -d {DB_NAME} -f '{args.input}/{file}'"
            print(f"running {command}")
            output_file = f"error.txt"
            f = open(str(output_file), "w")
            proc = subprocess.Popen(command, shell=True, env={
                        'PGPASSWORD': os.environ.get("PGPASSWORD")
                        },
                        stdout=f)
            proc.wait()
        except Exception as e:
            print('Exception happened during dump %s' %(e))
            quit()

def modify_sql(file_path):
    print(file_path)  # Do something with the file
    # Read the file content
    with file_path.open('r', encoding='utf-8') as file:
        content = file.read()
    
    # Remove the string 'temp_' from the content
    modified_content = content.replace('temp_', '')
    
    # Write the modified content back to the file
    with file_path.open('w', encoding='utf-8') as file:
        file.write(modified_content)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-a", "--all", action="store_true", default=False)
    parser.add_argument("-t", "--table", nargs="+", required=False, type=str, help="tables that should be restored")
    parser.add_argument("-i", "--input", required=True, help="path to the folder containing all the sql files")
    
    args = parser.parse_args()
    
    import_global_tables()
    sql_table = [
        "api_behavioroption",
        "api_behavioroptionstate",
        "api_behaviorframeoption",
        "api_xabslsymbolsparse",
        "api_cognitionrepresentation",
        "api_motionrepresentation",
        "api_image"
    ]
    for bla in sql_table:
        count = 0
        for file_path in sorted(Path(args.input).glob(f'{bla}_*.sql')):
            modify_sql(file_path)
            try:
                command = f"psql -h {DB_HOST} -p {DB_PORT} -U {DB_USER} -d {DB_NAME} -f '{file_path}'"
                print(f"running {command}")
                output_file = f"error.txt"
                f = open(str(output_file), "w")
                proc = subprocess.Popen(command, shell=True, env={
                            'PGPASSWORD': os.environ.get("PGPASSWORD")
                            },
                            stdout=f)
                proc.wait()
            except Exception as e:
                print('Exception happened during dump %s' %(e))
                quit()
            count += 1
            if count > 10:
                break


            

