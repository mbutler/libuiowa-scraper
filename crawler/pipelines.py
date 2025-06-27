import sqlite3
import os
from scrapy.exceptions import DropItem

class SQLitePipeline:
    def open_spider(self, spider):
        # Create data directory if it doesn't exist
        data_dir = 'data'
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)
        
        db_path = os.path.join(data_dir, "web_graph.db")
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        
        try:
            # Create nodes table (one entry per unique URL)
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS nodes (
                    url TEXT PRIMARY KEY,
                    title TEXT,
                    meta_description TEXT,
                    h1_text TEXT,
                    status_code INTEGER,
                    mime_type TEXT,
                    first_seen_depth INTEGER,
                    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Create edges table (one entry per parent-child relationship)
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS edges (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    parent_url TEXT,
                    child_url TEXT,
                    depth INTEGER,
                    discovered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    UNIQUE(parent_url, child_url)
                )
            ''')
            
            self.conn.commit()
            spider.logger.info(f"Database initialized at {db_path}")
        except Exception as e:
            spider.logger.error(f"Error creating database: {e}")
            raise

    def process_item(self, item, spider):
        try:
            # Insert or update node information
            self.cursor.execute('''
                INSERT OR REPLACE INTO nodes 
                (url, title, meta_description, h1_text, status_code, mime_type, first_seen_depth, last_updated)
                VALUES (?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
            ''', (
                item['url'],
                item.get('title'),
                item.get('meta_description'),
                item.get('h1_text'),
                item.get('status_code'),
                item.get('mime_type'),
                item.get('depth')
            ))
            
            # Insert edge relationship (if there's a parent)
            if item.get('parent_url'):
                try:
                    self.cursor.execute('''
                        INSERT OR IGNORE INTO edges (parent_url, child_url, depth)
                        VALUES (?, ?, ?)
                    ''', (
                        item.get('parent_url'),
                        item['url'],
                        item.get('depth')
                    ))
                except sqlite3.IntegrityError:
                    # Edge already exists, which is fine
                    pass
            
            self.conn.commit()
            spider.logger.debug(f"Saved item: {item['url']}")
            return item
        except Exception as e:
            spider.logger.error(f"Error saving item {item.get('url', 'unknown')}: {e}")
            raise DropItem(f"Failed to save item: {e}")

    def close_spider(self, spider):
        try:
            self.conn.close()
            spider.logger.info("Database connection closed")
        except Exception as e:
            spider.logger.error(f"Error closing database: {e}")
