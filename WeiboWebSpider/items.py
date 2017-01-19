# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class WeiboWebInfoItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    ID = scrapy.Field()             # 博主ID
    FanNum = scrapy.Field()         # 粉丝数量
    FollowerNum = scrapy.Field()    # 关注数量
    TweetsNum = scrapy.Field()      # 微博数量
    URL = scrapy.Field()            # 主页URL
    Tweets = scrapy.Field()         # 微博IDs

    NickName = scrapy.Field()       # 昵称
    Birthday = scrapy.Field()       # 生日
    City = scrapy.Field()           # 地区
    Gender = scrapy.Field()         # 性别
    # Marriage = scrapy.Field()       # 婚姻状况
    Signature = scrapy.Field()      # 简介


class WeiboWebTweetsItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    ID = scrapy.Field()             # 微博ID
    Content = scrapy.Field()        # 文字内容
    img_num = scrapy.Field()
    img_urls = scrapy.Field()       # 图片URL
    # PubTime = scrapy.Field()       # 发布时间（取消，暂不处理XX分钟前字样）
    Comments = scrapy.Field()       # 评论数量
    Like = scrapy.Field()           # 赞
    Transfer = scrapy.Field()       # 转发
    Tools = scrapy.Field()          # 发布工具
    # coordinates = scrapy.Field()    # 坐标
    URL = scrapy.Field()            # 微博评论页URL
