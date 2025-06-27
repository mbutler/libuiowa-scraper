import scrapy

class PageItem(scrapy.Item):
    url = scrapy.Field()
    parent_url = scrapy.Field()
    title = scrapy.Field()
    meta_description = scrapy.Field()
    h1_text = scrapy.Field()
    status_code = scrapy.Field()
    mime_type = scrapy.Field()
    depth = scrapy.Field()
