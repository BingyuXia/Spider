# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import Selector
from collect_ips.items import CollectIpsItem

class GetIpsSpider(scrapy.Spider):
    name = "get_ips"
    allowed_domains = ["xicidaili.com"]
    start_urls = ['http://xicidaili.com']
    
    def start_requests(self):
        reqs = []
        for i in range(1,10):
            req = scrapy.Request("http://www.xicidaili.com/nn/%s"%i)
            reqs.append(req)
            
        return reqs
        
    def parse(self, response):
        print("Into parse!")
        selector = Selector(response)
        #ip_list = response.xpath('//table[@id="ip_list"]')
        ip_list = selector.xpath('//table[@id="ip_list"]/tr')
        items = []
        for ip in ip_list[1:]:
            pre_item = CollectIpsItem()
            pre_item['IP'] = ip.xpath('td[2]/text()')[0].extract()
            pre_item['PORT'] = ip.xpath('td[3]/text()')[0].extract()
            pre_item['POSITION'] = ip.xpath('string(td[4])')[0].extract().strip()
            pre_item['TYPE'] = ip.xpath('td[6]/text()')[0].extract()
            pre_item['SPEED'] = ip.xpath('td[7]/div[@class="bar"]/@title').re('\d{0,2}\.\d{0,}')[0]
            pre_item['LAST_CHECK_TIME'] = ip.xpath('td[9]/text()')[0].extract()
            items.append(pre_item)
        return items

#//*[@id="ip_list"]/tbody/tr[2]/td[7]/div