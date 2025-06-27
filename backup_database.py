#!/usr/bin/env python3
"""
Backup script for the crawl database
Run this periodically during long crawls to create backups
"""

import sqlite3
import shutil
import os
from datetime import datetime

def backup_database():
    """Create a timestamped backup of the database"""
    try:
        source_path = os.path.join('data', 'web_graph.db')
        if not os.path.exists(source_path):
            print("Database not found.")
            return
        
        # Create backup directory if it doesn't exist
        backup_dir = 'backups'
        if not os.path.exists(backup_dir):
            os.makedirs(backup_dir)
        
        # Create timestamped backup filename
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_path = os.path.join(backup_dir, f'web_graph_backup_{timestamp}.db')
        
        # Copy the database
        shutil.copy2(source_path, backup_path)
        
        # Get stats for the backup
        conn = sqlite3.connect(source_path)
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM nodes")
        page_count = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM edges")
        link_count = cursor.fetchone()[0]
        conn.close()
        
        print(f"Backup created: {backup_path}")
        print(f"Pages in backup: {page_count:,}")
        print(f"Links in backup: {link_count:,}")
        print(f"Backup size: {os.path.getsize(backup_path) / 1024:.1f} KB")
        
    except Exception as e:
        print(f"Error creating backup: {e}")

if __name__ == "__main__":
    backup_database() 