import argparse
from pathlib import Path
import subprocess
import os
import re


# Custom key function for natural sorting
def natural_sort_key(s):
    # Use a regular expression to split the string into parts
    return [
        int(text) if text.isdigit() else text.lower()
        for text in re.split("([0-9]+)", str(s))
    ]


def import_global_tables():
    sql_table = [
        "api_event.sql",
        "api_game.sql",
        "api_log.sql",
        "api_logstatus.sql",
        "api_xabslsymbolcomplete.sql",
        "api_annotation.sql",
    ]

    for file in sql_table:
        try:
            command = f"psql -h {os.getenv('VAT_POSTGRES_HOST')} -p {os.getenv('VAT_POSTGRES_PORT')} -U {os.getenv('VAT_POSTGRES_USER')} -d {os.getenv('VAT_POSTGRES_DB')} -f '{args.input}/{file}'"
            print(f"running {command}")
            output_file = "error.txt"
            f = open(str(output_file), "w")
            proc = subprocess.Popen(
                command,
                shell=True,
                env={"PGPASSWORD": os.environ.get("PGPASSWORD")},
                stdout=f,
            )
            return_code = proc.wait()
            if return_code != 0:
                print(
                    f"Command failed with return code {return_code}. Aborting script."
                )
                quit()
        except Exception as e:
            print("Exception happened during dump %s" % (e))
            quit()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-i",
        "--input",
        required=True,
        help="path to the folder containing all the sql files",
    )
    parser.add_argument(
        "-t",
        "--table",
        nargs="+",
        required=False,
        type=str,
        help="tables that should be restored",
    )
    parser.add_argument(
        "--ids", nargs="+", required=False, type=int, help="ids that should be restored"
    )

    args = parser.parse_args()

    import_global_tables()

    sql_table = [
        "api_behavioroption",
        "api_behavioroptionstate",
        "api_behaviorframeoption",
        "api_xabslsymbolsparse",
        "api_cognitionframe",
        "api_motionframe",
        "api_cognitionrepresentation",
        "api_motionrepresentation",
        "api_image",
    ]
    for table in sql_table:
        if args.table:
            if table not in args.table:
                continue
        print(f"importing {table} tables")
        for file_path in sorted(
            Path(args.input).glob(f"{table}_*.sql"), key=natural_sort_key
        ):
            # if we have a list of ids, get the number of the file
            match = re.search(r"_(\d+)\.sql$", str(file_path))
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

            print(f"importing table for log id {number}")
            try:
                command = f"psql -h {os.getenv('VAT_POSTGRES_HOST')} -p {os.getenv('VAT_POSTGRES_PORT')} -U {os.getenv('VAT_POSTGRES_USER')} -d {os.getenv('VAT_POSTGRES_DB')} -f '{file_path}'"
                print(f"running {command}")
                output_file = "error.txt"
                f = open(str(output_file), "w")
                proc = subprocess.Popen(
                    command,
                    shell=True,
                    env={"PGPASSWORD": os.environ.get("PGPASSWORD")},
                    stdout=f,
                )
                return_code = proc.wait()
                if return_code != 0:
                    print(
                        f"Command failed with return code {return_code}. Aborting script."
                    )
                    quit()
            except Exception as e:
                print("Exception happened during dump %s" % (e))
                quit()
