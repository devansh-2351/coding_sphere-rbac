import asyncio
import sys
import os
from dotenv import load_dotenv

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

load_dotenv()

from sqlmodel import Session, create_engine
from models import User, Project
from auth import get_password_hash

def seed_database():
    """Seed the database with initial data."""
    # Use environment variable or default
    db_url = os.getenv("DATABASE_URL", "postgresql://postgres.pjtgbdtxinvnrjxnckmu:Toast%401234567890123@aws-0-ap-southeast-1.pooler.supabase.com:6543/postgres")
    engine = create_engine(db_url)
    
    with Session(engine) as session:
        # Check if users already exist
        existing_admin = session.query(User).filter(User.username == "admin").first()
        existing_user = session.query(User).filter(User.username == "user").first()
        
        if existing_admin and existing_user:
            print("Sample users already exist. Skipping user creation.")
        else:
            # Create admin user
            if not existing_admin:
                admin_user = User(
                    username="admin",
                    hashed_password=get_password_hash("admin123"),
                    role="admin"
                )
                session.add(admin_user)
                print("Created admin user")
            
            # Create regular user
            if not existing_user:
                regular_user = User(
                    username="user",
                    hashed_password=get_password_hash("user123"),
                    role="user"
                )
                session.add(regular_user)
                print("Created regular user")
            
            session.commit()
        
        # Get user IDs for project creation
        admin_user = session.query(User).filter(User.username == "admin").first()
        
        # Check if projects already exist
        existing_projects = session.query(Project).count()
        
        if existing_projects == 0:
            # Create sample projects
            projects = [
                Project(
                    name="Sample Project 1",
                    description="This is a sample project for testing",
                    created_by=admin_user.id
                ),
                Project(
                    name="Sample Project 2",
                    description="Another sample project",
                    created_by=admin_user.id
                )
            ]
            
            for project in projects:
                session.add(project)
            
            session.commit()
            print("Created sample projects")
        else:
            print("Sample projects already exist. Skipping project creation.")
        
        print("\nDatabase seeded successfully!")
        print("Admin user: username='admin', password='admin123'")
        print("Regular user: username='user', password='user123'")

if __name__ == "__main__":
    seed_database()
