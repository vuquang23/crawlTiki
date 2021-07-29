import scrapy
from crawlTiki.items import CrawltikiItem
import json

class TikiSpider(scrapy.Spider):
    name = 'tiki'
    allowed_domains = ['tiki.vn']
    start_urls = [
        "https://tiki.vn/api/v2/products?limit=48&include=advertisement&aggregations=1&trackity_id=e3570a34-cd3f-fb09-89cf-3589a304c9ee&category=10389&page=1&src=c.10389.hamburger_menu_fly_out_banner&urlKey=ao-crop-top",
        "https://tiki.vn/api/v2/products?limit=48&include=advertisement&aggregations=1&trackity_id=e3570a34-cd3f-fb09-89cf-3589a304c9ee&category=27582&page=1&src=c.27582.hamburger_menu_fly_out_banner&urlKey=dam-dang-xoe",
        "https://tiki.vn/api/v2/products?limit=48&include=advertisement&aggregations=1&trackity_id=e3570a34-cd3f-fb09-89cf-3589a304c9ee&category=27594&page=1&src=c.27594.hamburger_menu_fly_out_banner&urlKey=ao-cardigan-nu",
        "https://tiki.vn/api/v2/products?limit=48&include=advertisement&aggregations=1&trackity_id=e3570a34-cd3f-fb09-89cf-3589a304c9ee&category=49346&page=1&src=c.49346.hamburger_menu_fly_out_banner&urlKey=quan-ong-rong-nu",
        "https://tiki.vn/api/v2/products?limit=48&include=advertisement&aggregations=1&trackity_id=e3570a34-cd3f-fb09-89cf-3589a304c9ee&category=1509&page=1&src=c.1509.hamburger_menu_fly_out_banner&urlKey=ao-nguc",
        "https://tiki.vn/api/v2/products?limit=48&include=advertisement&aggregations=1&trackity_id=e3570a34-cd3f-fb09-89cf-3589a304c9ee&category=1685&page=1&src=c.1685.hamburger_menu_fly_out_banner&urlKey=ao-thun-nam-ngan-tay-khong-co",
        "https://tiki.vn/api/v2/products?limit=48&include=advertisement&aggregations=1&trackity_id=e3570a34-cd3f-fb09-89cf-3589a304c9ee&category=10380&page=1&src=c.10380.hamburger_menu_fly_out_banner&urlKey=ao-so-mi-nam-tay-ngan",
        "https://tiki.vn/api/v2/products?limit=48&include=advertisement&aggregations=1&trackity_id=e3570a34-cd3f-fb09-89cf-3589a304c9ee&category=922&page=1&src=c.922.hamburger_menu_fly_out_banner&urlKey=quan-tay-nam",
        "https://tiki.vn/api/v2/products?limit=48&include=advertisement&aggregations=1&trackity_id=e3570a34-cd3f-fb09-89cf-3589a304c9ee&category=10382&page=1&src=c.10382.hamburger_menu_fly_out_banner&urlKey=ao-hoodie-nam",
        "https://tiki.vn/api/v2/products?limit=48&include=advertisement&aggregations=1&trackity_id=e3570a34-cd3f-fb09-89cf-3589a304c9ee&category=27570&page=1&src=c.27570.hamburger_menu_fly_out_banner&urlKey=do-ngu-do-mac-nha-nam"
    ]

    def parse(self, response):
        my_bytes_value = response.body
        my_json = my_bytes_value.decode('utf8')
        data = json.loads(my_json)

        url = response.url
        collection_name = url[url.find('urlKey=') + len('urlKey=') : ]

        for good in data['data']:
            item = CrawltikiItem()
            item['name'] = good['name']
            item['price'] = good['price']
            item['list_price'] = good['list_price']
            item['url'] = good['url_path']
            item['img'] = good['thumbnail_url']
            item['rating'] = good['rating_average']
            item['collection_name'] = collection_name
            yield item

        if len(data['data']) == 0:
            return
        
        
        id = url.find('page=')
        pageNumber = 0
        newUrl = url[:id]
        while True:
            print(url[id])
            if url[id] == '&':
                newUrl = newUrl + 'page=' + str(pageNumber + 1) + url[id:]
                break
            else:
                if url[id].isnumeric():
                    pageNumber = pageNumber * 10 + int(url[id])
                id += 1

        yield response.follow(newUrl, callback=self.parse)
  