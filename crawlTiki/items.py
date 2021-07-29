# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class CrawltikiItem(scrapy.Item):
    name = scrapy.Field()
    price = scrapy.Field()
    list_price = scrapy.Field()
    url = scrapy.Field()
    img = scrapy.Field()
    rating = scrapy.Field()
    collection_name = scrapy.Field()