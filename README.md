E-Commerce-scraper
==================

###About

Scraper built with [Scrapy.](http://scrapy.org/) Scrapes emmi.rs and outputs all available products currently on site. Option to send [e-mail](https://docs.python.org/2/library/smtplib.html) and [sms message](https://www.twilio.com/) when scraping is finished.
Also included csv, json and xml files that Scrapy generates.

###Screenshot

![Screenshot](http://i.imgur.com/nitKLQg.png)

### Installation and Running
```
git clone https://github.com/Lazar-T/E-Commerce-scraper
cd E-Commerce-scraper
scrapy crawl emi
```
####To get csv output
```
scrapy crawl emi -o <filename>.csv
```



