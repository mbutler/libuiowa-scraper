import yaml
import sys
import os
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from crawler.spiders.universal_spider import UniversalSpider

def load_config():
    """Load and validate configuration"""
    try:
        with open('config.yaml', 'r') as f:
            config = yaml.safe_load(f)
        
        # Validate required fields
        if not config.get('start_urls'):
            raise ValueError("No start_urls specified in config.yaml")
        
        if not config.get('domains'):
            raise ValueError("No domains specified in config.yaml")
        
        return config
    except FileNotFoundError:
        print("Error: config.yaml not found")
        sys.exit(1)
    except yaml.YAMLError as e:
        print(f"Error parsing config.yaml: {e}")
        sys.exit(1)
    except ValueError as e:
        print(f"Configuration error: {e}")
        sys.exit(1)

def main():
    """Main function to run the crawler"""
    try:
        config = load_config()
        
        # Set the project settings path
        os.environ.setdefault('SCRAPY_SETTINGS_MODULE', 'crawler.settings')
        
        settings = get_project_settings()
        settings.set('DEPTH_LIMIT', config.get('depth', 3))
        settings.set('DOWNLOAD_DELAY', config.get('delay', 1.0))
        settings.set('ROBOTSTXT_OBEY', config.get('obey_robots', True))

        process = CrawlerProcess(settings)
        process.crawl(UniversalSpider, config=config)
        process.start()
        
    except KeyboardInterrupt:
        print("\nCrawler interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
