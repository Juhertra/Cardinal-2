import platform
import re
import subprocess
import os
from pathlib import Path
import shutil
from venv import logger
import psycopg2.errors
from django.db import connection

# Define the database configuration
POSTGRESQL_DB_NAME = "cardinaldb"
POSTGRESQL_USER = "postgres"
POSTGRESQL_PASS = "postgres"
POSTGRESQL_HOST = "localhost"
POSTGRESQL_PORT = 5432

DATABASE_CONFIG = {
    "default":{
        "ENGINE": "django.db.backends.postgresql",
        "NAME": POSTGRESQL_DB_NAME,
        "USER": POSTGRESQL_USER,
        "PASSWORD": POSTGRESQL_PASS,
        "HOST": POSTGRESQL_HOST,
        "PORT": POSTGRESQL_PORT,
}}

# Define Cardinal root path
BASE_DIR = Path(__file__).resolve().parent

# Define the PostgreSQL version
PG_VERSION = "15.2" # Replace with the version you want to install/configure

# Define the PostgreSQL installation directory for Windows
WINDOWS_POSTGRESQL_DIR = "C:\\Program Files\\PostgreSQL\\"

# Define the PostgreSQL BIN directory for Windows
WINDOWS_POSTGRESQL_BIN = "C:\\Program Files\\PostgreSQL\\{version}\\bin".format(version=PG_VERSION)

# Define the PostgreSQL installation directory for Linux and macOS
UNIX_POSTGRESQL_DIR = "/usr/local/pgsql/"

# Define the path to the Django settings module
SETTINGS_MODULE = "cardinal.settings"


POSTGRESQL_INSTALLER = "postgresql.exe"

# Get the platform name (Windows, Linux, or macOS)
PLATFORM = platform.system()

def main():
    try:
        # Check if PostgreSQL is installed
        if PLATFORM == "Windows":
            print("Running script on Windows environment")
            postgresql_installed = os.path.exists(WINDOWS_POSTGRESQL_DIR)

            # Check if PostgreSQL executable exists in the base path
            print("checking if {file} was downloaded".format(file=POSTGRESQL_INSTALLER))
            is_executable = check_executable_exist(POSTGRESQL_INSTALLER)

            # Check if PostgreSQL bin already exists in PATH environment variable
            print("Checking if PostgreSQL bin directory is in the existing PATH environment variable...")
            is_bin = check_bin_to_path(WINDOWS_POSTGRESQL_BIN)

        else:
            print("Running script on linux based environment")
            postgresql_installed = os.path.exists(UNIX_POSTGRESQL_DIR)

        # Install PostgreSQL if not installed
        if not postgresql_installed:
            if PLATFORM == "Windows":
                if not is_executable:
                    # Download the PostgreSQL installer for Windows
                    print("PostgreSQL is not installed. Downloading...")
                    download_windows_file(POSTGRESQL_INSTALLER, PG_VERSION)
                
                # and run it with the silent install option
                print("Installing...")
                execute_windows_file(POSTGRESQL_INSTALLER)
                        
            else:
                # Install PostgreSQL on Linux or macOS using the system package manager
                print("PostgreSQL is not installed. Installing...")
                macos_linux_download_execute_file()

        # Add PostgreSQL bin directory to PATH if not already added
        
        if not is_bin:
            print("Adding {postgresql_bin_path} directory to the existing PATH environment variable".format(postgresql_bin_path=WINDOWS_POSTGRESQL_BIN))
            add_bin_to_path(WINDOWS_POSTGRESQL_BIN) 
        
        # Remove "." and rest of numbers
        curated_version = PG_VERSION.split(".")[0]

        # Check PostgreSQL status
        print("Checking PostgreSQL is running...")
        pg_status = check_db(PLATFORM, curated_version)

        if pg_status.returncode != 0:
            print("PostgreSQL is not running, starting PostgreSQL...")
            # Start the PostgreSQL server
            start_db(PLATFORM, curated_version)
            # Check PostgreSQL status again
            pg_status = check_db(PLATFORM, curated_version)
            if pg_status.returncode != 0:
                raise psycopg2.errors.SqlclientUnableToEstablishSqlconnection("PostgreSQL failed to start.")

        print("PostgreSQL is running...")

        # Replace the DATABASES setting in settings.py with the hardcoded one
        replace_db_config(BASE_DIR)

        create_cardinal_db(POSTGRESQL_DB_NAME, POSTGRESQL_USER, POSTGRESQL_PASS, POSTGRESQL_HOST, POSTGRESQL_PORT)

        print("PostgreSQL installed and configured successfully!")
    
    except Exception as e:
        print(f"Error: {e}")
        exit(1)

    exit(0)


def execute_windows_file(file):
    try:
        subprocess.run([
                file,
                "--unattendedmodeui",
                "none",
                "--mode",
                "unattended"
            ],
            check=True,
        )
    except subprocess.CalledProcessError as error:
        # Log the error and raise an exception
        logger.error(f"Error executing {file}: {error}")
        raise error
    finally:
        # Remove the file, even if an exception was raised
        os.remove(file)


def download_windows_file(file, version):
    subprocess.run([
            "powershell",
            "Invoke-WebRequest",
            "https://get.enterprisedb.com/postgresql/postgresql-{version}-1-windows-x64.exe".format(version=version),
            "-OutFile",
            os.path.abspath(file),
        ],
        check=True,
    )


def macos_linux_download_execute_file():
    package_manager = None
    if PLATFORM == "Linux":
        if shutil.which("apt-get"):
            package_manager = "apt-get"
        elif shutil.which("yum"):
            package_manager = "yum"
        else:
            print("Unsupported Linux distribution. Exiting...")
            exit(1)
    elif PLATFORM == "Darwin":
        if shutil.which("brew"):
            package_manager = "brew"
        else:
            print("Homebrew is not installed. Exiting...")
            exit(1)
    if package_manager:
        subprocess.run([package_manager, "update"], check=True)
        subprocess.run([package_manager, "install", "-y", "postgresql"], check=True)

def replace_db_config(root_dir):
    for dirpath, dirnames, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename == 'settings.py':
                path = os.path.join(dirpath, filename)
                with open(path, 'r+') as f:
                    content = f.read()
                    f.seek(0)
                    f.truncate()
                    content = re.sub(
                        r'DATABASES\s*\=\s*\{[^{}]*\'default\'\s*\:\s*\{[^{}]*\}\s*[^{}]*\}',
                        'DATABASES = {\n"default": {\n"ENGINE": "django.db.backends.postgresql",\n "NAME": "' + POSTGRESQL_DB_NAME + '",\n "USER": "' + POSTGRESQL_USER + '",\n "PASSWORD": "' + POSTGRESQL_PASS + '",\n "HOST": "' + POSTGRESQL_HOST + '",\n "PORT": "' + str(POSTGRESQL_PORT) + '"\n}\n}',
                        content
                    )
                    f.write(content)

def start_db(platform, version):
    # Start the PostgreSQL server
    if platform == 'Windows':
        subprocess.run(['pg_ctl', 'start', '-D', 'C:\Program Files\PostgreSQL\{version}\data'.format(version=version)])
    elif platform == 'darwin':
        subprocess.run(['/Library/PostgreSQL/{version}/bin/pg_ctl', 'start', '-D', '/Library/PostgreSQL/{version}/data'.format(version=version)])
    else:
        subprocess.run(['sudo', '-u', 'postgres', 'pg_ctl', 'start', '-D', '/etc/postgresql/{version}/main'.format(version=version)])

def check_db(platform, version):
    # Check PostgreSQL status
    if platform == 'Windows':
        status = subprocess.run(['pg_ctl', 'status', '-D', 'C:\Program Files\PostgreSQL\{version}\data'.format(version=version)], stdout=subprocess.PIPE, text=True)
    elif platform == 'darwin':
        status = subprocess.run(['/Library/PostgreSQL/{version}/bin/pg_ctl', 'status', '-D', '/Library/PostgreSQL/{version}/data'.format(version=version)], stdout=subprocess.PIPE, text=True)
    else:
        status = subprocess.run(['sudo', '-u', 'postgres', 'pg_ctl', 'status', '-D', '/etc/postgresql/{version}/main'.format(version=version)], stdout=subprocess.PIPE, text=True)
    return status

def check_executable_exist(file):
    #Check if PostgreSQL executable exists in the base path
    if not os.path.join(file):
        print("{executable} not found".format(executable=file))
        return False
    else:    
        print("found {executable} file.".format(executable=file))
        return True


def check_bin_to_path(bin_dir):
    """
    Check if PostgreSQL bin directory is in PATH environment variable.
    """
    bin_path = bin_dir
    path_var = os.environ.get("PATH")
    if path_var is None:
        return False
    paths = path_var.split(":")
    for path in paths:
        if path == bin_path:
            return True
    return False

def add_bin_to_path(bin_path):
    os.environ["PATH"] = bin_path + os.pathsep + os.environ["PATH"]
    print("PostgreSQL bin directory is already in the existing PATH environment variable")

import psycopg2

def create_cardinal_db(dbname, dbuser, dbpassword, dbhost, dbport):
    # Replace the values in <> with your own values
    conn = psycopg2.connect(
        dbname='postgres',
        user=dbuser,
        password=dbpassword,
        host=dbhost,
        port=dbport
    )

    # Set autocommit to True
    conn.autocommit = True

    # Open a cursor to perform database operations
    cur = conn.cursor()

    # Replace <new_database_name> with the name of the new database you want to create
    cur.execute("CREATE DATABASE {};".format(dbname))

    # Close the cursor and connection
    cur.close()
    conn.close()

'''
TODO:
    Create Django admin user
    python manage.py createsuperuser
    user: cardinal
    password: cardinal
'''


main()