import sqlite3
import scrapy
from urllib.parse import urljoin, urlparse
from ..items import PageItem

class UniversalSpider(scrapy.Spider):
    name = "universal"

    def __init__(self, config=None, *args, **kwargs):
        super(UniversalSpider, self).__init__(*args, **kwargs)
        self.config = config or {}
        self.allowed_domains = self.config.get('domains', [])
        self.start_urls = self.config.get('start_urls', [])
        self.seen_urls = set()
        self.strict_domain = self.config.get('strict_domain', False)
        # Set depth limit to None by default (no limit), but respect config if set
        self.depth_limit = self.config.get('depth', None)
        
        # Load previously seen URLs from database for resume capability
        self._load_seen_urls()

    def _load_seen_urls(self):
        """Load previously crawled URLs from database to enable resume"""
        try:
            import os
            db_path = os.path.join('data', 'web_graph.db')
            if os.path.exists(db_path):
                conn = sqlite3.connect(db_path)
                cursor = conn.cursor()
                cursor.execute("SELECT url FROM nodes")
                for (url,) in cursor.fetchall():
                    self.seen_urls.add(url)
                conn.close()
                self.logger.info(f"Loaded {len(self.seen_urls)} previously crawled URLs for resume")
        except Exception as e:
            self.logger.warning(f"Could not load previous URLs for resume: {e}")

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url, callback=self.parse, meta={'depth': 0})

    def parse(self, response):
        if response.url in self.seen_urls:
            return
        self.seen_urls.add(response.url)

        try:
            item = PageItem()
            item['url'] = response.url
            item['parent_url'] = response.meta.get('parent_url')
            item['title'] = self._clean_text(response.xpath('//title/text()').get())
            item['meta_description'] = self._clean_text(response.xpath('//meta[@name="description"]/@content').get())
            item['h1_text'] = self._clean_text(response.xpath('//h1/text()').get())
            item['status_code'] = response.status
            item['mime_type'] = self._safe_decode_content_type(response.headers.get('Content-Type', b''))
            item['depth'] = response.meta.get('depth', 0)

            yield item

            # Check if we should continue crawling based on depth
            current_depth = response.meta.get('depth', 0)
            should_continue = True
            
            if self.depth_limit is not None:
                should_continue = current_depth < self.depth_limit
            
            if should_continue:
                for href in response.css('a::attr(href)').getall():
                    try:
                        absolute_url = urljoin(response.url, href)
                        parsed = urlparse(absolute_url)
                        # Strict domain logic
                        if self.strict_domain:
                            if parsed.netloc.endswith('lib.uiowa.edu'):
                                yield response.follow(
                                    absolute_url,
                                    callback=self.parse,
                                    meta={
                                        'parent_url': response.url,
                                        'depth': current_depth + 1
                                    }
                                )
                        else:
                            if parsed.netloc in self.allowed_domains:
                                yield response.follow(
                                    absolute_url,
                                    callback=self.parse,
                                    meta={
                                        'parent_url': response.url,
                                        'depth': current_depth + 1
                                    }
                                )
                    except Exception as e:
                        self.logger.warning(f"Error processing link {href}: {e}")
                        
        except Exception as e:
            self.logger.error(f"Error processing {response.url}: {e}")

    def _clean_text(self, text):
        """Clean text by stripping whitespace and newlines"""
        if text is None:
            return None
        return text.strip()

    def _safe_decode_content_type(self, content_type):
        """Safely decode Content-Type header"""
        try:
            return content_type.decode('utf-8')
        except (UnicodeDecodeError, AttributeError):
            return str(content_type)
