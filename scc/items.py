# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Item, Field

class SccListItem(Field):
    id = Field()
    url = Field()
    pub_time = Field()
    state = Field()

class SccLastItem(Field):
    id=Field()
    title=Field()
    pub_time=Field()
    pick_time=Field()
    url=Field()
    data_source_name=Field()
    data_source_type=Field()
    web_type=Field()
    category=Field()
    content=Field()
    img_path=Field()
    attachment_path=Field()
    media_path=Field()
    issued_number=Field()
    content_source=Field()
    issued_unit=Field()