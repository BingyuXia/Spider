# -*- coding: utf-8 -*-

import scrapy
import re
import datetime
from scrapy.selector import Selector
from guba.items import PostItem, PostContentItem
#from selenium import webdriver




class GubaSpiderSpider(scrapy.Spider):
    
    name = "guba_spider"
    allowed_domains = ['guba.eastmoney.com/']
    start_urls = ['http://guba.eastmoney.com/remenba.aspx?type=1']
    host = "http://guba.eastmoney.com/"

    def __init__(self):
        #self.driver=webdriver.Chrome(chromedriver)
        self.page = 10    #主页抓取页数
        self.page2 = 3   #评论抓取页数
        self.time = datetime.datetime(2017, 8, 4, 22, 10, 0)   #抓取某时间线之后的内容
        return
        
    def start_requests(self):
        req = scrapy.Request(url="http://guba.eastmoney.com/remenba.aspx?type=1",
                             callback = self.get_underlying_parse
                             )
        yield req

    def get_underlying_parse(self, response):
        selector = Selector(response)
        for underlying_class in selector.xpath('//div[@class="ngbggulbody"]/div')[:1]:   #市场
            for underlying in underlying_class.xpath('ul/li')[:1]:                           #标的
                underlying_ID =  underlying.xpath('a/text()').re('(\d{6})')[0]           
                #print(underlying_ID +" has been searched!")
                url = underlying.xpath('a/@href').extract()[0]
                url = self.host + url
                yield scrapy.Request(url=url, 
                                    callback=self.get_post_parse,
                                    meta={'ID':underlying_ID},
                                    dont_filter=True,
                                    )


        return
    
    def get_post_parse(self, response):
        print("open post successfully:" , response.meta['ID'])
        selector = Selector(response)
        #self.driver.get(response.url)
        postslist = selector.xpath('//*[@id="articlelistnew"]/div')
        underlying_ID = response.meta['ID']
        

        for post in postslist:                            
            #One_page
            if post.xpath('span[3]/em/text()') != []:              #过滤掉第一页开头帖子
                continue
            
            if post.xpath("@class").extract_first() == "articleh":
                update_time = post.xpath('span[6]/text()').extract_first()
                update_time = datetime.datetime.strptime("2017-"+update_time,"%Y-%m-%d  %H:%M")   #跨年的时候要注意！
                if update_time < self.time:
                    break
                post_item = PostItem()
                post_item['ID'] = underlying_ID
                post_item['READ'] = post.xpath('span[1]/text()').extract_first()
                post_item['COMMENT'] = post.xpath('span[2]/text()').extract_first()
                post_item['TITLE'] = post.xpath('span[3]/a/text()').extract_first()
                post_url = self.host + post.xpath('span[3]/a/@href').extract_first()[1:]
                post_url = re.sub(r'\.html', ",d.html", post_url)
                post_item['URL'] = post_url
                post_item['WRITER'] = post.xpath('span[4]/a/text()').extract_first()
                post_item['TIME'] = post.xpath('span[5]/text()').extract_first()
                #yield post_item
                yield scrapy.Request(url = post_url,
                                     callback = self.get_post_parse2,
                                     meta={'TITLE':post_item['TITLE'], 'ID':post_item['ID'], 'TIME':post_item['TIME']},
                                     dont_filter = True,
                                     )
#                break
            #Next_page
            elif post.xpath("@class").extract()[0] == "pager":
                #this_page = post.xpath('span/span/a[@class="on"]/text()').extract_first()
                url_n = response.url
                url_n = url_n.split('_')
                if len(url_n)==1:
                    this_page = 1
                    root = re.sub(r'\.html$',"",url_n[0])
                elif len(url_n)==2:  
                    page = url_n[1].split('.')
                    this_page = int(page[0])
                    root = url_n[0]
                if this_page < self.page:
                    #next_page = post.xpath('span/span/a')[-2]
                    next_page = this_page+1
                    #url = self.post + next_page.xpath('@href').extract_first()
                    url = "%s_%s.html" % (root, str(next_page))
                    yield scrapy.Request(url = url,
                                         callback=self.get_post_parse,
                                         meta={'ID':underlying_ID},
                                         dont_filter = True,
                                         )
            
        return 

    def get_post_parse2(self, response):
        selector = Selector(response)
        contents = PostContentItem()
        contents['TITLE'] = response.meta['TITLE']
        contents['ID'] = response.meta['ID']
        contents['TIME'] = response.meta['TIME']
        print(response)
        #Contents       
        print(response.url)
        if selector.xpath('//*[@id="zwconbody"]/div/div')==[]:
            content = selector.xpath('//*[@id="zwconbody"]/div/text()').extract()
            contents["CONTENT"] = [c.strip() for c in content]
#            print(contents['CONTENT'])
        else:
            p_list = selector.xpath('//*[@id="zwconbody"]/div/div[@id="zw_body"]/p')
            content = ""
            for p in p_list:
                ret_text = p.xpath('text()').extract_first()
                if ret_text != None:
                    content += ret_text
                    content += "\n"
            contents['CONTENT'] = content
        #Comments
        comments = []  #评论
        times = []     #时间
        faces = []      #表情
        comments_responses = selector.xpath('//*[@id="zwlist"]/div')
        if comments_responses == []:
            contents['COMMENT'] = []
            print("No comments")
        else:
            for com_ind in comments_responses:
                id_data = com_ind.xpath('@class').extract_first()
                if id_data == "zwli clearfix":
                    _time = com_ind.xpath('div[3]/div/div[2]/text()').extract_first()[4:]
                    times.append(_time)
#                    print(_time)
                    _time = datetime.datetime.strptime(_time,"%Y-%m-%d  %H:%M:%S")
                    if _time > self.time:
                        comment = com_ind.xpath('div[3]/div/div[@class="zwlitext stockcodec"]/text()').extract()
                        face_ret = com_ind.xpath('div[3]/div/div[@class="zwlitext stockcodec"]/img')
                        face = [i.xpath('@title').extract_first() for i in face_ret]
                        #[@class="zwlitext stockcodec"]
                        if len(comments) == 0:
                            print("The first comment")
                        elif comment == comments[-1] and times[-1] == times[-2]:
                            times.pop()
                            break
                        comments.append(comment)
                        faces.append(face)
                    else:
                        break
                elif id_data == "pager talc zwpager":
                    break
                    url_n = response.url
                    url_n = url_n.split('_')
                    if len(url_n)==1:
                        this_page = 1
                        root = re.sub(r'\.html$',"",url_n[0])
                    elif len(url_n)==2:  
                        page = url_n[1].split('.')
                        this_page = int(page[0])
                        root = url_n[0]
                    if this_page < self.page2:
                        #next_page = post.xpath('span/span/a')[-2]
                        next_page = this_page+1
                        #url = self.post + next_page.xpath('@href').extract_first()
                        url = "%s_%s.html" % (root, str(next_page))
                        yield scrapy.Request(url = url,
                                         callback=self.get_post_parse2,
                                         meta={'TITLE':contents['TITLE'], 'ID': contents['ID']},
                                         dont_filter = True,
                                         )
            contents['COMMENT'] = comments
            contents['FACE'] = faces 
        yield contents
            
        

            
            