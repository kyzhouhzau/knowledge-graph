# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class OmimprojectItem(scrapy.Item):
    # define the fields for your item here like:
    gene = scrapy.Field()
    mutation = scrapy.Field()
    MIM = scrapy.Field()
    disease = scrapy.Field()
    article = scrapy.Field()
