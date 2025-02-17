import argparse
from pathlib import Path
import subprocess
import os
import re

class ImportLog:
    def __init__(self, log_file="import_log.txt"):
        """
        Initializes the ImportLog class.
        :param log_file: Path to the log file.
        """
        self.log_file = log_file
        
        # Ensure the log file exists
        if not os.path.exists(self.log_file):
            with open(self.log_file, "w") as f:
                f.write("# Import Log - Processed Files\n")

    def log(self, filename: str):
        """
        Logs a new file entry with a timestamp.
        :param filename: Name of the processed file.
        """
        if not self.is_logged(filename):
            with open(self.log_file, "a") as f:
                f.write(f"{filename}\n")

    def is_logged(self, filename: str) -> bool:
        """
        Checks if a file has already been logged.
        :param filename: Name of the file to check.
        :return: True if the file is logged, False otherwise.
        """
        with open(self.log_file, "r") as f:
            return any(filename in line for line in f)
        
    def delete_log(self):
        """
        Clears the log file.
        """
        Path(self.log_file).unlink()


# Custom key function for natural sorting
def natural_sort_key(s):
    # Use a regular expression to split the string into parts
    return [int(text) if text.isdigit() else text.lower() for text in re.split('([0-9]+)', str(s))]


def import_global_tables():
    sql_table = [
        "schema.sql",
        "auth_group.sql",
        "django_content_type.sql",
        "auth_permission.sql",
        "auth_group_permissions.sql",
        "user_organization.sql",
        "user_vatuser.sql",
        "authtoken_token.sql",
        "django_admin_log.sql",
        "django_migrations.sql",
        "django_session.sql",
        "user_vatuser_groups.sql",
        "user_vatuser_user_permissions.sql",
        "api_event.sql",
        "api_game.sql",
        "api_log.sql",
        "api_logstatus.sql",
        "api_xabslsymbolcomplete.sql",
        "api_annotation.sql"
    ]

    for file in sql_table:
        try:
            command = f"psql -h {os.getenv('VAT_POSTGRES_HOST')} -p {os.getenv('VAT_POSTGRES_PORT')} -U {os.getenv('VAT_POSTGRES_USER')} -d {os.getenv('VAT_POSTGRES_DB')} -f '{args.input}/{file}'"
            print(f"running {command}")
            output_file = f"error.txt"
            f = open(str(output_file), "w")
            proc = subprocess.Popen(command, shell=True, env={
                        'PGPASSWORD': os.environ.get("PGPASSWORD")
                        },
                        stdout=f)
            return_code = proc.wait()
            if return_code != 0:
                print(f"Command failed with return code {return_code}. Aborting script.")
                quit()
        except Exception as e:
            print('Exception happened during dump %s' %(e))
            quit()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", required=True, help="path to the folder containing all the sql files")
    parser.add_argument("-t", "--table", nargs="+", required=False, type=str, help="tables that should be restored")
    parser.add_argument("--ids",  nargs="+", required=False, type=int, help="ids that should be restored")
    
    args = parser.parse_args()
    import_log = ImportLog()

    #import_global_tables()

    sql_table = [
        "api_behavioroption",
        "api_behavioroptionstate",
        "api_behaviorframeoption",
        "api_xabslsymbolsparse",
        "api_image",
        "api_motionrepresentation",
        "api_cognitionrepresentation",
    ]
    for table in sql_table:
        if args.table:
            if table not in args.table:
                continue
        print(f"importing {table} tables")
        for file_path in sorted(Path(args.input).glob(f'{table}_*.sql'), key=natural_sort_key):
            # if we have a list of ids, get the number of the file
            match = re.search(r'_(\d+)\.sql$', str(file_path))
            if match:
                # Extract the number from the match object
                number = int(match.group(1))
            else:
                print("ERROR: could not parse number of ")
                quit()
            if args.ids:                
                # Check if the number is in the list of numbers
                if number not in args.ids:
                    continue

            # check if we already done the insert for this sql file
            if import_log.is_logged(str(file_path)):
                print(f"skipping {file_path}")
                continue
            # TODO else check if data is there for the table and id
            print(f"importing table for log id {number}")
            try:
                command = f"psql -h {os.getenv('VAT_POSTGRES_HOST')} -p {os.getenv('VAT_POSTGRES_PORT')} -U {os.getenv('VAT_POSTGRES_USER')} -d {os.getenv('VAT_POSTGRES_DB')} -f '{file_path}'"
                print(f"running {command}")
                output_file = f"error.txt"
                f = open(str(output_file), "w")
                proc = subprocess.Popen(command, shell=True, env={
                            'PGPASSWORD': os.environ.get("PGPASSWORD")
                            },
                            stdout=f)
                return_code = proc.wait()
                if return_code != 0:
                    print(f"Command failed with return code {return_code}. Aborting script.")
                    quit()
                else:
                    import_log.log(str(file_path))
            except Exception as e:
                print('Exception happened during dump %s' %(e))
                quit()

    import_log.delete_log()