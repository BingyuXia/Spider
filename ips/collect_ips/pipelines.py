# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymong as mg


class CollectIpsPipeline(object):
	def __init__(self):
		host = settings.MONGODB_HOST
        port = settings.MONGODB_PORT
        db_name = settings.MONGODB_DBNAME
        col_name = settings.MONGODB_COLNAME
        client = pymongo.MongoClient(host, port)
        self.col = client[db_name][col_name]

    def process_item(self, item, spider):
        with open("ips.txt", "a") as f:
        	doc = {"IP": item["IP"], "PORT": item["PORT"]}
        	self.col.insert_one()
            f.write("IP:"+str(item['IP'])+"   POSITION: "+str(item['POSITION']))
            f.write("\n")
        return item 
