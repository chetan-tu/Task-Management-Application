import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv
import os
import time

# Load the correct environment file based on the TESTING flag
if os.getenv("TESTING") == "true":
    env_path = os.path.join("tests", ".env.test")  # Path to test environment file
else:
    env_path = os.path.join(os.path.dirname(__file__), ".env")  # Path to main environment file
load_dotenv(dotenv_path=env_path)

# Database configuration from environment variables
DATABASE_CONFIG = {
    "host": os.getenv("DATABASE_HOST"),
    "database": os.getenv("DATABASE_NAME"),
    "user": os.getenv("DATABASE_USER"),
    "password": os.getenv("DATABASE_PASSWORD")
}

# Function to establish a database connection with retry logic
def get_connection():
    while True:
        try:
            connection = psycopg2.connect(
                host=DATABASE_CONFIG["host"],
                database=DATABASE_CONFIG["database"],
                user=DATABASE_CONFIG["user"],
                password=DATABASE_CONFIG["password"],
                cursor_factory=RealDictCursor
            )
            return connection
        except psycopg2.OperationalError as e:
            print("Error connecting to the database:", e)
            print("Retrying in 5 seconds...")
            time.sleep(5)

# Function to check if the tasks table exists
def table_exists(connection, table_name="task"):
    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT EXISTS (
                    SELECT FROM information_schema.tables 
                    WHERE table_name = %s
                );
            """, (table_name,))
            return cursor.fetchone()['exists']
    except Exception as e:
        print(f"Error checking if table '{table_name}' exists:", e)
        return False

# Function to create the tasks table
def create_tasks_table():
    connection = get_connection()
    if connection is None:
        print("Failed to connect to the database.")
        return

    if table_exists(connection, "task"):
        print("Table 'task' already exists.")
    else:
        print("Creating 'task' table...")
        try:
            with connection.cursor() as cursor:
                cursor.execute("""
                    CREATE TABLE task (
                        id SERIAL PRIMARY KEY,
                        title VARCHAR(255) NOT NULL,
                        description TEXT,
                        status VARCHAR(50),
                        created_at TIMESTAMP DEFAULT NOW(),
                        updated_at TIMESTAMP DEFAULT NOW()
                    );
                """)
                connection.commit()
                print("Tasks table created successfully.")
        except Exception as e:
            print("Error creating the 'task' table:", e)
        finally:
            connection.close()

# Run the table creation function
create_tasks_table()
print("Database connection successful")
