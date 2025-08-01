"""
Database setup script for local development
Run this script to create the PostgreSQL database and user
"""
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import sys

def create_database():
    """Create the PostgreSQL database and user for the application."""
    # Database configuration
    DB_NAME = "fastapi_rbac"
    DB_USER = "fastapi_user"
    DB_PASSWORD = "fastapi_password"
    DB_HOST = "localhost"
    DB_PORT = "5432"

    try:
        # Connect to PostgreSQL server (default database)
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            user="postgres",  # Default PostgreSQL superuser
            password=input("Enter PostgreSQL superuser password: ")
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor()
        
        # Create user if not exists
        cursor.execute(f"""
            DO $$
            BEGIN
                IF NOT EXISTS (SELECT FROM pg_catalog.pg_roles WHERE rolname = '{DB_USER}') THEN
                    CREATE USER {DB_USER} WITH PASSWORD '{DB_PASSWORD}';
                END IF;
            END
            $$;
        """)
        
        # Create database if not exists
        cursor.execute(f"""
            SELECT 1 FROM pg_catalog.pg_database WHERE datname = '{DB_NAME}'
        """)
        exists = cursor.fetchone()
        
        if not exists:
            cursor.execute(f"CREATE DATABASE {DB_NAME} OWNER {DB_USER}")
            print(f"Database '{DB_NAME}' created successfully!")
        else:
            print(f"Database '{DB_NAME}' already exists.")
        
        # Grant privileges
        cursor.execute(f"GRANT ALL PRIVILEGES ON DATABASE {DB_NAME} TO {DB_USER}")
        
        cursor.close()
        conn.close()
        
        print(f"Database setup completed!")
        print(f"Database URL: postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}")
        
        # Create .env file
        with open('.env', 'w') as f:
            f.write(f"DATABASE_URL=postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}\n")
            f.write("SECRET_KEY=your-super-secret-key-change-this-in-production\n")
            f.write("ACCESS_TOKEN_EXPIRE_MINUTES=30\n")
        
        print("Created .env file with database configuration.")
        
    except psycopg2.Error as e:
        print(f"Error setting up database: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    create_database()
