from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.loader import ItemLoader
from emmiScraper.items import EmmiscraperItem
from scrapy.contrib.loader.processor import Compose, MapCompose
from w3lib.html import replace_escape_chars, remove_tags
from scrapy.selector import HtmlXPathSelector
from scrapy.selector import Selector
from scrapy.http import Request
import urlparse



class EmmiSpider(CrawlSpider):
    name = "emi"
    allowed_domains = ["emmi.rs"]
    start_urls = [
        "http://emmi.rs/konfigurator/proizvodi.10.html?go=true&Id=10&productTitle=a&brandId=&categoryId=&price=&discount=&advanced_search=1&limit=1000&offset=0"

    ]

    def parse(self, response):
        hxs = Selector(response)
        item_selector = hxs.xpath('//*[@class="productListTitle"]/a/@href').extract()
        products = hxs.xpath('//*[@class="productListTitle"]/a/text()').extract()
        for url, product in zip(item_selector, products):
            yield Request(urlparse.urljoin(response.url, url),
                          callback=self.parse_item,
                          meta={'product': product}
                          )



    def parse_item(self, response):
        l = ItemLoader(item=EmmiscraperItem(), response=response)
        hxs = HtmlXPathSelector(response)
        l.default_output_processor = MapCompose(lambda v: v.strip(), replace_escape_chars)
        l.add_value('product', response.meta['product'])
        l.add_xpath('img_url', '/html/body/div[3]/div[4]/div[2]/div[2]/div[1]/div[1]/div[1]/a/img/@src')
        l.add_xpath('description', '//*[@class="productListText widthFull noPadding"]/text()')
        l.add_xpath('price', '//*[@class="price"]/text()')
        l.add_value('url_of_item', response.url)
        return l.load_item()


