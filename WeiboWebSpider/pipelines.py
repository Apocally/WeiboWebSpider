# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
from WeiboWebSpider.items import *


class MongoDBPipleline(object):
    def __init__(self):
        self.client = pymongo.MongoClient("localhost", 27017)
        self.db = self.client["Weibo"]
        self.Information = self.db["Information"]
        self.Tweets = self.db["Tweets"]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        """ 判断item的类型，并作相应的处理，再入数据库 """
        if isinstance(item, WeiboWebInfoItem):
            try:
                self.Information.insert(dict(item))
            except:
                pass
        elif isinstance(item, WeiboWebTweetsItem):
            try:
                self.Tweets.insert(dict(item))
            except:
                pass
        return item
