#!/usr/bin/env python3
import sqlite3
from pathlib import Path

def check_db():
    db_path = Path("src/lcpi/db/aep_prices.db")
    print(f"Checking database: {db_path}")
    
    if not db_path.exists():
        print("Database not found")
        return
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Check tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = cursor.fetchall()
    print(f"Tables: {tables}")
    
    # Check diameters table structure
    cursor.execute("PRAGMA table_info(diameters)")
    columns = cursor.fetchall()
    print(f"Diameter table columns: {columns}")
    
    # Check some data
    cursor.execute("SELECT * FROM diameters LIMIT 5")
    data = cursor.fetchall()
    print(f"Sample data: {data}")
    
    conn.close()

if __name__ == "__main__":
    check_db()