import argparse
from pathlib import Path
import subprocess
import os
import psycopg2
from psycopg2 import sql
import time

# kubectl port-forward postgres-postgresql-0 -n postgres 1234:5432

DB_HOST="localhost"
DB_PORT="1234"
DB_USER="naoth"
DB_NAME="vat"

conn = psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=os.environ.get("PGPASSWORD")
    )

def get_all_log_ids():
    # Create a cursor object
    cur = conn.cursor()
    query = sql.SQL("SELECT DISTINCT id FROM api_log;")
    cur.execute(query)

    # Fetch all results
    results = cur.fetchall()

    # Convert the results to a list of ids
    id_list = [row[0] for row in results]

    # Close the cursor and connection
    cur.close()
    
    return sorted(id_list)

def create_temp_table(table, table_name, log_id):
    delete_temp_table(table_name)

    cur = conn.cursor()
    query = sql.SQL(f"CREATE TABLE {table_name} AS SELECT * FROM {table} WHERE log_id_id = {log_id}")
    cur.execute(query)
    conn.commit()
    cur.close()


def delete_temp_table(table_name):
    cur = conn.cursor()
    query = sql.SQL(f"DROP TABLE IF EXISTS {table_name}")
    cur.execute(query)
    cur.close()


def export_full_tables():
    tables = [
        "api_event",
        "api_game",
        "api_log",
        "api_logstatus",
        "api_xabslsymbolcomplete",
        "api_annotation"
    ]
    for table in tables:
        try:
            command = f"pg_dump -h {DB_HOST} -p {DB_PORT} -U {DB_USER} -d {DB_NAME} -t {table} --data-only"
            print(f"running {command} > {table}.sql")
            output_file = Path(args.output) / f"{table}.sql"
            f = open(str(output_file), "w")
            proc = subprocess.Popen(command, shell=True, env={
                        'PGPASSWORD': os.environ.get("PGPASSWORD")
                        },
                        stdout=f)
            proc.wait()
        except Exception as e:
            print('Exception happened during dump %s' %(e))


def export_split_table(log_id):
    tables = [
        "api_behaviorframeoption",
        "api_behavioroption",
        "api_behavioroptionstate",
        "api_cognitionrepresentation",
        "api_motionrepresentation",
        "api_image",
        "api_xabslsymbolsparse"
    ]
    for table in tables:
        output_file = Path(args.output) / f"{table}_{log_id}.sql"
        if output_file.exists():
            continue

        try:
            temp_table_name = f"temp_{table}"
            create_temp_table(table, temp_table_name, log_id)
            command = f"pg_dump -h {DB_HOST} -p {DB_PORT} -U {DB_USER} -d {DB_NAME} -t {temp_table_name} --data-only"
            print(f"\trunning {command} > {table}_{log_id}.sql")

            f = open(str(output_file), "w")

            proc = subprocess.Popen(command, shell=True, env={
                        'PGPASSWORD': os.environ.get("PGPASSWORD")
                        },
                        stdout=f)
            proc.wait()

            delete_temp_table(temp_table_name)
        except Exception as e:
            print('Exception happened during dump %s' %(e))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-a", "--all", action="store_true", default=False)
    parser.add_argument("-l", "--logs", nargs="+", required=False, type=int, help="Log Id's separated by space")
    parser.add_argument("-o", "--output", required=True, help="Output folder for all sql files")
    parser.add_argument("-g", "--global_tables", action="store_true", required=False, default=False, help="")

    args = parser.parse_args()
    Path(args.output).mkdir(exist_ok=True, parents=True)
    
    if args.global_tables:
        print("will export tables that are the same for all log ids")
        export_full_tables()

    if args.logs:
        for log_id in args.logs:
            print(f"exporting data for log {log_id}")
            t0 = time.time()
            export_split_table(log_id)
            t1 = time.time()
            print(f"time to export: {t1-t0}s")
        
    elif args.all:
        log_ids = get_all_log_ids()
        
        for log_id in log_ids:
            print(f"exporting data for log {log_id}")
            t0 = time.time()
            export_split_table(log_id)
            t1 = time.time()
            print(f"time to export: {t1-t0}s")
    else:
        print("ERROR: either specify all or logs argument")
        print(parser.print_help())
        quit()

    
    conn.close()