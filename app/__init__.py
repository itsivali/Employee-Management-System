import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models import Base

DATABASE_URL = 'sqlite:///employee_management.db'

def init_app():
    """Initialize the application and database."""
    # Ensure the database exists
    if not os.path.exists('employee_management.db'):
        print("Creating database...")
        engine = create_engine(DATABASE_URL)
        Base.metadata.create_all(engine)
    else:
        print("Database already exists.")

    # Create a new SQLAlchemy session
    engine = create_engine(DATABASE_URL)
    Session = sessionmaker(bind=engine)
    return Session()

# Function to run the CLI
def run_cli():
    """Run the CLI application."""
    from .cli import cli
    cli(obj={'session': init_app()})

if __name__ == "__main__":
    run_cli()
