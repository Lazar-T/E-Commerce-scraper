# -*- coding: utf-8 -*-

# Scrapy settings for emmiScraper project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'emmiScraper'

SPIDER_MODULES = ['emmiScraper.spiders']
NEWSPIDER_MODULE = 'emmiScraper.spiders'

DOWNLOADER_MIDDLEWARES = {
        'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
        'emmiScraper.rotate_useragent.RotateUserAgentMiddleware': 400
    }

# Crawl responsibly by identifying yourself (and your website) on the user-agent
# USER_AGENT = 'emmiScraper (+http://www.yourdomain.com)'
