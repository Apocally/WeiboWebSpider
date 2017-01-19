# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html
import random
from WeiboWebSpider.sa_sp import get_cookies_list
from WeiboWebSpider.UserAgents import agents
from WeiboWebSpider.sa_sp import myWeiBo


class UserAgentMiddleware(object):
    """ 换User-Agent """

    def process_request(self, request, spider):
        agent = random.choice(agents)
        request.headers["User-Agent"] = agent


class CookiesMiddleware(object):
    """ 换Cookie """
    def __init__(self):
        self.myWeibo = myWeiBo
        self.cookies_list = get_cookies_list()

    def process_request(self, request, spider):
        cookie = random.choice(self.cookies_list)
        request.cookies = cookie
