E-Commerce-scraper
==================

### About

Spider built with [Scrapy](http://scrapy.org/). Scrapes [emmi.rs](http://emmi.rs/naslovna_stranica.1.html) and gets all available products. Option to send [e-mail](https://docs.python.org/2/library/smtplib.html) and [sms message](https://www.twilio.com/) when scraping is finished. Uses rotating user agents.
Also included `csv`, `json` and `xml` files that Scrapy can generate.

### Screenshot

![Screenshot](http://i.imgur.com/nitKLQg.png)

### Installation and Running
```
git clone https://github.com/Lazar-T/E-Commerce-scraper
cd E-Commerce-scraper
scrapy crawl emi
```

For e-mail and sms notification `emmiScraper/spiders/emmi.py` file should be updated. Methods that require modifications are: `send_email` and `send_sms`.

**Note:** For sending sms message using Twilio, free registration on [twilio.com](https://www.twilio.com/) would be nesesarry.

