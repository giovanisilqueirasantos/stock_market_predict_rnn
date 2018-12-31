# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ScrapersItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    date = scrapy.Field()
    cotation = scrapy.Field()
    minimum = scrapy.Field()
    maximum = scrapy.Field()
    value_variation = scrapy.Field()
    volume = scrapy.Field()
    pass
