import smtplib
import urlparse

from scrapy import signals
from scrapy.http import Request
from scrapy.loader import ItemLoader
from scrapy.spiders import CrawlSpider
from twilio.rest import TwilioRestClient
from scrapy.selector import HtmlXPathSelector
from w3lib.html import replace_escape_chars, remove_tags
from scrapy.loader.processors import Compose, MapCompose

from emmiScraper.items import EmmiscraperItem


class EmmiSpider(CrawlSpider):
    name = 'emi'
    allowed_domains = ['emmi.rs']
    start_urls = ['http://emmi.rs/konfigurator/proizvodi.10.html?go=true&Id=10&advanced_search=1&productTitle=&x=0&y=0&limit=-1&offset=0']

    def parse(self, response):
        """Yields url for every item currently available on the site, and
           transports every product name to parse_item method.

        @url http://emmi.rs/konfigurator/proizvodi.10.html?advanced_search=1&productTitle=&x=0&y=0
        @scrapes urls products

        """
        urls = response.xpath('//*[@class="productListTitle"]/a/@href').extract()
        products = response.xpath('//*[@class="productListTitle"]/a/text()').extract()

        for url, product in zip(urls, products):
            yield Request(urlparse.urljoin(response.url, url),
                          callback=self.parse_item,
                          meta={'product': product}
                          )

    def parse_item(self, response):
        """Returns fields: url_of_item, product, img_url, description, and price."""

        l = ItemLoader(item=EmmiscraperItem(), response=response)
        l.default_output_processor = MapCompose(lambda v: v.strip(), replace_escape_chars)

        l.add_value('url_of_item', response.url)
        l.add_value('product', response.meta['product'])
        l.add_xpath('img_url', '/html/body/div[3]/div[4]/div[2]/div[2]/div[1]/div[1]/div[1]/a/img/@src')
        l.add_xpath('description', '//*[@class="productListText widthFull noPadding"]/text()')
        l.add_xpath('price', '//*[@class="price"]/text()[2]')

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

            headers = ['From: ' + sender,
            'Subject: ' + subject,
            'To: ' + reciever,
            'MIME-Version: 1.0',
            'Content-Type: text/html']
            headers = '\r\n'.join(headers)

            session = smtplib.SMTP(smtp_server)

            session.ehlo()
            session.starttls()
            session.ehlo()
            session.login(sender, sender_password)

            session.sendmail(sender, reciever, headers + '\r\n\r\n' + body)
            session.quit()

        send_email('username', 'password', 'smtp.gmail.com:587',
        'to', 'message', 'cca')

    def send_sms(self, spider):
        account_sid = ''
        auth_token = ''
        client = TwilioRestClient(account_sid, auth_token)
        message = (client.sms.messages.create(body='', to='',
        from_=''))
