#!/usr/bin/env python3
"""
Monitor script to check crawl progress
Run this while the crawler is running to see progress
"""

import sqlite3
import time
import os
from datetime import datetime

def get_crawl_stats():
    """Get current crawl statistics"""
    try:
        db_path = os.path.join('data', 'web_graph.db')
        if not os.path.exists(db_path):
            print("Database not found. Crawler may not have started yet.")
            return
        
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Get basic stats
        cursor.execute("SELECT COUNT(*) FROM nodes")
        total_pages = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM edges")
        total_links = cursor.fetchone()[0]
        
        # Get depth distribution
        cursor.execute("""
            SELECT first_seen_depth, COUNT(*) 
            FROM nodes 
            GROUP BY first_seen_depth 
            ORDER BY first_seen_depth
        """)
        depth_stats = cursor.fetchall()
        
        # Get recent activity (last 10 pages)
        cursor.execute("""
            SELECT url, title, last_updated 
            FROM nodes 
            ORDER BY last_updated DESC 
            LIMIT 5
        """)
        recent_pages = cursor.fetchall()
        
        conn.close()
        
        # Display stats
        print(f"\n{'='*50}")
        print(f"CRAWL PROGRESS - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'='*50}")
        print(f"Total Pages Crawled: {total_pages:,}")
        print(f"Total Links Found: {total_links:,}")
        print(f"Database Size: {os.path.getsize(db_path) / 1024:.1f} KB")
        
        print(f"\nDepth Distribution:")
        for depth, count in depth_stats:
            print(f"  Depth {depth}: {count:,} pages")
        
        print(f"\nRecent Activity (Last 5 pages):")
        for url, title, timestamp in recent_pages:
            clean_title = title[:50] + "..." if title and len(title) > 50 else title
            print(f"  {clean_title}")
            print(f"    {url}")
            print(f"    {timestamp}")
            print()
        
    except Exception as e:
        print(f"Error getting stats: {e}")

def main():
    """Main monitoring loop"""
    print("Crawl Monitor - Press Ctrl+C to stop")
    print("Checking progress every 30 seconds...")
    
    try:
        while True:
            get_crawl_stats()
            time.sleep(30)
    except KeyboardInterrupt:
        print("\nMonitoring stopped.")

if __name__ == "__main__":
    main() 