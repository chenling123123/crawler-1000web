# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
#import warnings

from scc.items import SccLastItem,SccListItem
from scc.model.item_models import list_item, details_item, engine
from sqlalchemy.orm import sessionmaker

class SccPipeline(object):
    #warnings.filterwarnings('error')
    def process_item(self, item, spider):
        if isinstance(item, SccListItem):
            try:
                self.session.add(list_item(**item))
                self.session.commit()
                return item
            except:
                self.session.rollback()
                print("入库出错")
        elif isinstance(item, SccLastItem):
            try:
                self.session.add(details_item(**item))
                self.session.commit()
                return item
            except:
                self.session.rollback()
                print("入库出错")

    def open_spider(self, spider):
        Session = sessionmaker(bind=engine)
        self.session = Session()

    def close_spider(self, spider):

        self.session.close()