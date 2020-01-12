# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ChengxingspiderItem(scrapy.Item):
    # define the fields for your item here like:
    fund_code = scrapy.Field()
    fund_name = scrapy.Field()
    fund_price = scrapy.Field()
    date = scrapy.Field()
