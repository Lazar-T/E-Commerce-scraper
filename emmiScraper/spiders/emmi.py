from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.loader import ItemLoader
from emmiScraper.items import EmmiscraperItem
from scrapy.contrib.loader.processor import Compose, MapCompose
from w3lib.html import replace_escape_chars, remove_tags
from scrapy.selector import HtmlXPathSelector
from scrapy.selector import Selector
from scrapy.http import Request
from twilio.rest import TwilioRestClient
from scrapy import signals
import urlparse
import smtplib



class EmmiSpider(CrawlSpider):
    name = "emi"
    allowed_domains = ["emmi.rs"]
    start_urls = [
        "http://emmi.rs/konfigurator/proizvodi.10.html?go=true&Id=10&productTitle=a&brandId=&categoryId=&price=&discount=&advanced_search=1&limit=10&offset=0"

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
        l.add_xpath('price', '//*[@class="price"]/text()[2]')
        l.add_value('url_of_item', response.url)
        return l.load_item()


    @classmethod        
    def from_crawler(cls, crawler):
        spider = cls()
        crawler.signals.connect(spider.sending_email, signals.spider_closed)
        crawler.signals.connect(spider.send_sms, signals.spider_closed)
        return spider


    def sending_email(self, spider):
        def send_email(sender, sender_password, smtp_server, reciever, message, subject):
            body = "" + message + ""

            headers = ["From: " + sender,
            "Subject: " + subject,
            "To: " + reciever,
            "MIME-Version: 1.0",
            "Content-Type: text/html"]
            headers = "\r\n".join(headers)

            session = smtplib.SMTP(smtp_server)

            session.ehlo()
            session.starttls()
            session.ehlo()
            session.login(sender, sender_password)

            session.sendmail(sender, reciever, headers + "\r\n\r\n" + body)
            session.quit()

        send_email("username", "password", "smtp.gmail.com:587",
        "to", "message", "cca")


    def send_sms(self, spider):
        account_sid = ""
        auth_token = ""
        client = TwilioRestClient(account_sid, auth_token)
        message = (client.sms.messages.create(body='', to="",
        from_=""))
    
