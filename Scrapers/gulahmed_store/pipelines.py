# -*- coding: utf-8 -*-
from pymongo import MongoClient
import urllib.request
import base64
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


class GulahmedStorePipeline(object):
    def __init__(self):
        self.client=MongoClient("localhost",27017)
        db=self.client.get_database('scraped_data')
        self.collection=db.all_brands

    def process_item(self, item, spider):

        links = item['img_url']
        resource = urllib.request.urlopen(links)
        bin=base64.b64encode(resource.read())
        item['Binary']=bin
        filename=item['img_url'].split('/')[-1]
        item['filename'] = filename

        self.collection.update({'prod_page':item['prod_page']}, {"$setOnInsert": dict(item)}, upsert= True)
        return item
