import os
from urllib.parse import quote_plus
from sqlalchemy import create_engine, inspect, text
from sqlalchemy.orm import sessionmaker

def get_db_connection(host, port, database, user, password):
    """
    Create a SQLAlchemy engine with the provided database credentials.
    
    Args:
        host (str): Database host
        port (int): Database port
        database (str): Database name
        user (str): Database username
        password (str): Database password
        
    Returns:
        SQLAlchemy engine
        
    Raises:
        Exception: If database connection fails
    """
    try:
        # URL encode the password to handle special characters like @
        encoded_password = quote_plus(password)
        
        # Use the encoded password in the connection string
        engine = create_engine(
            f"mysql+pymysql://{user}:{encoded_password}@{host}:{port}/{database}"
        )
        
        # Test the connection
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
        return engine
    except Exception as e:
        raise Exception(f"Database connection failed: {str(e)}")

def create_session(engine):
    """
    Create a SQLAlchemy session from an engine.
    
    Args:
        engine: SQLAlchemy engine
        
    Returns:
        SQLAlchemy sessionmaker
    """
    return sessionmaker(bind=engine)