# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html

from proxy import get_ip
from user_agents import agents

class UserAgentMiddleware(object):
    #换User-Agent
    def process_request(self, request, spider):
        agent = random.choice(agents)
        request.headers["User-Agent"] = agent

class RandomProxyMiddleware(object):
    #动态设置ip代理
    def process_request(self, request, spider):
        request.meta["proxy"] = get_ip()