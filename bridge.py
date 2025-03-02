import os
from fastapi import APIRouter, HTTPException, Query, Body
from sqlalchemy import create_engine, inspect, text
from datetime import datetime
from sqlalchemy.orm import sessionmaker
from pydantic import BaseModel
from typing import Any, Dict
from urllib.parse import quote_plus

def get_db_connection(host, port, database, user, password):
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
    
router = APIRouter()

# Hardcode DB details for initial testing
DB_DETAILS = {
    "host": os.getenv("DB_HOST", "localhost"),
    "port": 3306,
    "database": "dbname",
    "user": "username",
    "password": "password",
}

# Create an engine and session
engine = get_db_connection(**DB_DETAILS)
Session = sessionmaker(bind=engine)

class SoftDeletePayload(BaseModel):
    deleted_by_guid: int

@router.get("/test")
def test_db_connection():
    try:
        engine = get_db_connection(**DB_DETAILS)
        return {"message": "Database connection successful"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Utility function to get columns of a table
def get_table_columns(table_name: str):
    """Fetch the columns for a given table from the database"""
    inspector = inspect(engine)
    columns = inspector.get_columns(table_name)
    return {column['name']: column['type'] for column in columns}

def generate_dynamic_model(table_name: str):
    """Generate a Pydantic model dynamically based on table columns"""
    columns = get_table_columns(table_name)
    dynamic_model = type(
        f"{table_name.capitalize()}Model", 
        (BaseModel,), 
        {col: (str, ...) for col in columns}  # Simple str type for now, can be extended
    )
    return dynamic_model

# Create dynamic CRUD operations for any table
from sqlalchemy import text

@router.get("/base/{table_name}")
def get_all_records(table_name: str, page: int = Query(1, ge=1), limit: int = Query(10, ge=1)):
    """Fetch all records from the given table with pagination"""
    session = Session()

    # Calculate the offset based on the page number and limit
    offset = (page - 1) * limit
    
    try:
        # Query to get the records with pagination
        query = text(f"SELECT * FROM {table_name} LIMIT :limit OFFSET :offset")
        result = session.execute(query, {"limit": limit, "offset": offset}).fetchall()

        # Query to get the total number of records for pagination metadata
        count_query = text(f"SELECT COUNT(*) FROM {table_name}")
        total_records = session.execute(count_query).scalar()

        # Convert result to list of dictionaries
        columns = [column['name'] for column in inspect(engine).get_columns(table_name)]
        result_dict = [dict(zip(columns, row)) for row in result]

        # Prepare pagination metadata
        pagination = {
            "total_records": total_records,
            "limit": limit,
            "skip": offset,
            "total_pages": (total_records // limit) + (1 if total_records % limit else 0),
            "current_page": page,
        }

        return {
            "data": result_dict,
            "pagination": pagination
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error reading table: {str(e)}")

@router.post("/base/{table_name}")
def create_record(table_name: str, record: Dict[str, Any] = Body(...)):
    """Insert a new record into the table"""
    session = Session()
    try:
        # Create placeholders for the values
        columns = ", ".join(record.keys())
        placeholders = ", ".join([f":{key}" for key in record.keys()])
        
        # Create the query using text()
        query = text(f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})")
        
        # Execute with parameters
        session.execute(query, record)
        session.commit()
        
        return {"message": f"Record added to {table_name}"}
    
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=f"Error inserting record: {str(e)}")
    
    finally:
        session.close()

@router.put("/base/{table_name}/{record_id}")
def update_record(table_name: str, record_id: int, record: Dict[str, Any] = Body(...)):
    """Update an existing record in the table"""
    session = Session()
    try:
        # Create placeholders for the SET clause
        set_clause = ", ".join([f"{key}=:{key}" for key in record.keys()])
        
        # Create the query using text()
        query = text(f"UPDATE {table_name} SET {set_clause} WHERE id = :record_id")
        
        # Add record_id to the parameters
        params = {**record, "record_id": record_id}
        
        # Execute with parameters
        session.execute(query, params)
        session.commit()
        
        return {"message": f"Record {record_id} updated in {table_name}"}
    
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=f"Error updating record: {str(e)}")
    
    finally:
        session.close()

@router.delete("/base/{table_name}/{record_id}")
def soft_delete_record(
    table_name: str, 
    record_id: int,
    payload: SoftDeletePayload = Body(...)
):
    """Soft delete a record by updating active, deleted flags and deletion metadata"""
    session = Session()
    try:
        current_time = int(datetime.now().timestamp())
        
        query = text(f"""
            UPDATE {table_name} 
            SET active = 0, 
                deleted = 1, 
                deleted_by_guid = :deleted_by_guid,
                deleted_at = :deleted_at
            WHERE id = :record_id
        """)
        
        params = {
            "record_id": record_id,
            "deleted_by_guid": payload.deleted_by_guid,
            "deleted_at": current_time
        }
        
        result = session.execute(query, params)
        session.commit()
        
        if result.rowcount == 0:
            raise HTTPException(
                status_code=404, 
                detail=f"Record {record_id} not found in {table_name}"
            )
            
        return {
            "message": f"Record {record_id} soft deleted from {table_name}",
            "deleted_at": current_time,
            "deleted_by": payload.deleted_by_guid
        }
    
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=f"Error soft deleting record: {str(e)}")
    
    finally:
        session.close()

@router.delete("/base/{table_name}/{record_id}/hard")
def delete_record(table_name: str, record_id: int):
    """Delete a record from the table by ID"""
    session = Session()
    try:
        # Create the query using text()
        query = text(f"DELETE FROM {table_name} WHERE id = :record_id")
        
        # Execute with parameters
        session.execute(query, {"record_id": record_id})
        session.commit()
        
        return {"message": f"Record {record_id} deleted from {table_name}"}
    
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=f"Error deleting record: {str(e)}")
    
    finally:
        session.close()

# Why Patch method? Unlike PUT which typically requires sending the complete resource, PATCH is designed for partial updates
@router.patch("/base/{table_name}/{record_id}")
def patch_record(table_name: str, record_id: int, record: Dict[str, Any] = Body(...)):
    """Update specific fields of a record"""
    session = Session()
    try:
        # Create placeholders for the SET clause
        set_clause = ", ".join([f"{key}=:{key}" for key in record.keys()])
        
        # Create the query using text()
        query = text(f"UPDATE {table_name} SET {set_clause} WHERE id = :record_id")
        
        # Add record_id to the parameters
        params = {**record, "record_id": record_id}
        
        result = session.execute(query, params)
        session.commit()

        if result.rowcount == 0:
            raise HTTPException(
                status_code=404, 
                detail=f"Record {record_id} not found in {table_name}"
            )
            
        return {"message": f"Record {record_id} patched in {table_name}"}
    
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=f"Error patching record: {str(e)}")
    
    finally:
        session.close()