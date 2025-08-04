#!/usr/bin/env python3
import sqlite3

conn = sqlite3.connect('src/lcpi/db/bois_test_sqlite.db')
cursor = conn.cursor()

# Lister les tables
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = cursor.fetchall()
print("Tables créées:")
for table in tables:
    print(f"  - {table[0]}")
    
    # Afficher la structure de chaque table
    cursor.execute(f"PRAGMA table_info({table[0]})")
    columns = cursor.fetchall()
    print(f"    Colonnes:")
    for col in columns:
        print(f"      {col[1]} ({col[2]})")
    print()

conn.close() 