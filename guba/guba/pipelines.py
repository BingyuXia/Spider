# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
#import pymongo
#from scrapy.conf import settings
from guba.items import PostItem, PostContentItem


class GubaPipeline(object):
    def __init__(self):
        host = settings['MONGODB_HOST']
        port = settings['MONGODB_PORT']
        db_name = settings['MONGODB_DBNAME']
        col_name = settings['MONGODB_COLNAME']
        client = pymongo.MongoClient(host, port)
        self.col = client[db_name][col_name]
    
    def process_item(self, item, spider):
        if isinstance(item, POSTItem):
            try:
                doc = {key:item[key] for key in item}
                self.col.insert_one(doc)
            except:
                pass
                
        if isinstance(item, POSTContentItem):
            try:
                doc = {"CONTENT" : item["CONTENT"],
                       "COMMENTS": item["COMMENT"],
                       "FACE"    : item["FACE"] 
                        }
                query = {"ID"    : item["ID"]
                         "TITLE" : item["TITLE"]
                         "TIME"  : item["TIME"]
                          }
                self.col.update_one(query, {'$set' : doc})
            except:
                pass
                
                
        self.data_one.insert(item)
        return item
"""
class GubaPipeline(object):
    def __init__(self):
        pass
    def process_item(self, item, spider):
        if isinstance(item, PostItem):
            try:
                print(item["TITLE"])
                # print(item["READ"])
                # print(item["COMMENT"])
                # print(item["TIME"])
                # print(item["WRITER"])
            except:
                pass
        if isinstance(item, PostContentItem):
            try:
                pass
#                 print(item["TITLE"])
#                 print(item["CONTENT"])
# #                print(item["TIME"])
# #                print(item["ID"])
#                 print(item["COMMENT"])
#                  print(item["FACE"])
            except:
                pass
"""