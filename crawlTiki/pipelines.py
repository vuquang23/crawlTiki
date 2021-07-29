import pymongo  
from crawlTiki.items import CrawltikiItem

class MongoPipeline(object):  

   def __init__(self, mongo_uri, mongo_db): 
        self.mongo_uri = mongo_uri 
        self.mongo_db = mongo_db 

   @classmethod 
   def from_crawler(cls, crawler): 
        return cls( 
            mongo_uri = crawler.settings.get('MONGO_URI'), 
            mongo_db = crawler.settings.get('MONGO_DATABASE', 'items') 
        ) 
  
   def open_spider(self, spider): 
        self.client = pymongo.MongoClient(self.mongo_uri) 
        self.db = self.client[self.mongo_db] 

   def close_spider(self, spider): 
        self.client.close() 

   def process_item(self, item, spider): 
        item_changed = CrawltikiItem()
        item_changed['name'] = item['name']
        item_changed['price'] = item['price']
        item_changed['list_price'] = item['list_price']
        item_changed['url'] = item['url']
        item_changed['img'] = item['img']
        item_changed['rating'] = item['rating']
        self.db[item['collection_name']].insert(dict(item_changed)) 
        return item_changed