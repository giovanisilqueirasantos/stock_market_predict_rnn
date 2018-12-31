# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo
from datetime import datetime

class MongoPipeline(object):
    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]
        if spider.name in self.db.collection_names():
            self.db[spider.name].drop()
        if 'date_1' not in sorted(list(self.db.profiles.index_information())):
            self.db.profiles.create_index([('date', pymongo.ASCENDING)], unique=True)

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        if item['cotation'] != 'None':
            splited_date = item['date'].split('/')
            item['date'] = datetime(int(splited_date[2]), int(splited_date[1]), int(splited_date[0]))
            item['cotation'] = float(item['cotation'])
            item['minimum'] = float(item['minimum'])
            item['maximum'] = float(item['maximum'])
            item['value_variation'] = float(item['value_variation'])
            item['volume'] = float(item['volume'])
            self.db[spider.name].insert_one(dict(item))
        return item