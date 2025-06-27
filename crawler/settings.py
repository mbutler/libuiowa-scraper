BOT_NAME = 'crawler'

SPIDER_MODULES = ['crawler.spiders']
NEWSPIDER_MODULE = 'crawler.spiders'

ITEM_PIPELINES = {
    'crawler.pipelines.SQLitePipeline': 1
}

LOG_LEVEL = 'INFO'

# User agent to identify the crawler
USER_AGENT = 'libuiowa-scraper/1.0 (+https://github.com/your-repo)'

# Respect robots.txt
ROBOTSTXT_OBEY = True

# Configure a delay for requests for the same website (default: 0)
DOWNLOAD_DELAY = 1.0

# Enable or disable downloader middlewares
DOWNLOADER_MIDDLEWARES = {
   'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
}

# Enable and configure HTTP caching
HTTPCACHE_ENABLED = True
HTTPCACHE_EXPIRATION_SECS = 3600
HTTPCACHE_DIR = 'httpcache'

# Progress logging for long crawls
LOG_STATS_INTERVAL = 60  # Log stats every 60 seconds

# AutoThrottle for better performance
AUTOTHROTTLE_ENABLED = True
AUTOTHROTTLE_START_DELAY = 1
AUTOTHROTTLE_MAX_DELAY = 60
AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
AUTOTHROTTLE_DEBUG = False
