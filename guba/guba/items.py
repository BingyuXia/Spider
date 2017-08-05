# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class PostItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    ID  = scrapy.Field()    #标的代码
    URL = scrapy.Field()    #帖子链接
    TITLE = scrapy.Field()   #帖子题目
    READ = scrapy.Field()  #阅读数
    COMMENT = scrapy.Field()  #评论数
    TIME  =  scrapy.Field() #发表日期
    WRITER = scrapy.Field()  #发帖者

class PostContentItem(scrapy.Item):
    ID = scrapy.Field()          #标的代码
    TITLE = scrapy.Field()       #帖子题目
    TIME = scrapy.Field()        #发表日期
    CONTENT = scrapy.Field()     #内容
    COMMENT = scrapy.Field()     #评论
    FACE = scrapy.Field()        #表情
