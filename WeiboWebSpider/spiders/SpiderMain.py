import re
from WeiboWebSpider.items import *
import scrapy


def url_generator_for_id(_id):
    tweet_url = 'http://weibo.cn/u/%s?filter=1' % _id   # 只显示原创
    follower_url = 'http://weibo.cn/%s/follow' % _id
    return tweet_url, follower_url


def url_generator_from_follow_him(follow_url):
    try:
        pa = re.compile(r'uid=(.*?)&')
        _id = pa.search(follow_url).group(1)
        tweet_url, follower_url = url_generator_for_id(_id)
        return tweet_url, follower_url
    except:
        return None


def find_basic_info(target, basic_info_html):
    try:
        pa = re.compile(r'%s:(.*?)<' % target)
        content = pa.search(basic_info_html).group(1)
    except:
        content = ''
    return content


def img_extractor(html_content):  # xpath遇到不存在节点就报错，特殊处理
    img_num, img_urls = '', ''
    flag = 0
    try:
        if html_content.xpath("div[1]/a[1]/text()") is not None and html_content.xpath("div[1]/a[1]/text()").extract_first()[:3] == '组图共':   # 组图流
            content = html_content.xpath("div[1]").extract_first()
            img_urls = re.findall("\[<a href=\"(.*?)\">组图共", content)[0]
            img_num = html_content.xpath("div[1]/a[1]/text()").extract_first()[3]
            flag = 1
    except:
        pass
    try:
        if html_content.xpath("div[1]/span[@class='ctt']/a/text()") is not None and html_content.xpath("div[1]/span[@class='ctt']/a/text()").extract_first()[-4:] == '秒拍视频' and flag is not 1:   #视频流
            content = html_content.xpath("div[1]/span[@class='ctt']").extract_first()
            img_num = 'video'
            img_urls = re.findall("href=\"(.*?)\">.*?秒拍视频", content)[0]
            flag = 2
    except:
        pass
    try:
        if html_content.xpath("div[2]/a[1]/img") is not None and flag is not 1 and flag is not 2:   # 一图流
            content = html_content.xpath("div[2]/a[2]").extract_first()
            img_urls = re.findall("href=\"(.*?)\">原图", content)[0]
            img_num = '1'
    except:
        pass

    return img_num, img_urls


class WeiboWebSpider(scrapy.Spider):
    name = 'WeiboWebSpider'
    start_ids = [
        '5501440198',      # 测试
        '2936059657'      # GIF博士
    ]

    # 避免重复抓取
    # start_urls = ['2936059657']
    # tweets_list = []
    #
    # scrawl_ID = set(start_urls)  # 记录待爬的微博ID
    # finish_ID = set()  # 记录已爬的微博ID

    def start_requests(self):   # meta用来传递参数
        for each_id in self.start_ids:
            tweet_url, follower_url = url_generator_for_id(each_id)
            yield scrapy.Request(tweet_url, callback=self.parse_tweet)
            yield scrapy.Request(tweet_url, callback=self.parse_info)
            yield scrapy.Request(follower_url, callback=self.parse_follower)

    def parse_follower(self, response):
        selector = scrapy.Selector(response)
        for each_follower in selector.xpath(r"body/table"):
            follow_url = each_follower.xpath("tr/td[2]/a[2]/@href").extract_first()   # tbody标签为浏览器自动加上，解析时不需加入
            tweet_url, follower_url = url_generator_from_follow_him(follow_url)
            yield scrapy.Request(tweet_url, callback=self.parse_tweet)
            yield scrapy.Request(tweet_url, callback=self.parse_info)
            yield scrapy.Request(follower_url, callback=self.parse_follower)
        try:
            next_page = selector.xpath(r"body/div[@class='pa']/form/div/a/@href").extract_first()
            next_page = 'http://weibo.cn' + next_page
            yield scrapy.Request(url=next_page, callback=self.parse_follower)
        except:
            pass

    def parse_tweet(self, response):
        selector = scrapy.Selector(response)
        for each_tweet in selector.xpath(r"body/div[@class='c' and @id]"):
            item = WeiboWebTweetsItem()
            try:
                item['ID'] = each_tweet.xpath('@id').extract_first()
                item['Content'] = each_tweet.xpath("div[1]/span[@class='ctt']/text()").extract_first()
                item['img_num'], item['img_urls'] = img_extractor(each_tweet)
                if item['img_num'] == 'video' or item['img_num'] == '':
                    text_content = each_tweet.xpath("div[1]").extract_first()
                else:
                    text_content = each_tweet.xpath("div[2]").extract_first()
                #item['PubTime'] = re.findall(">(.*?) 来自", text_content)
                item['Tools'] = re.findall("来自(.*?)<", text_content)[0]
                item['Comments'] = re.findall("评论\[(.*?)\]<", text_content)[0]
                item['Like'] = re.findall("赞\[(.*?)\]<", text_content)[0]
                item['Transfer'] = re.findall("转发\[(.*?)\]<", text_content)[0]
                item['URL'] = re.findall("href=\"(.*?)\"", text_content)[-2]
            except:
                pass
            yield item
        # 尝试寻找下一页并生成Request
        try:
            next_page = selector.xpath(r"body/div[@class='pa']/form/div/a/@href").extract_first()
            next_page = 'http://weibo.cn' + next_page
            yield scrapy.Request(url=next_page, callback=self.parse_tweet)
        except:
            pass

    def parse_info(self, response):
        selector = scrapy.Selector(response)
        item = WeiboWebInfoItem()
        info = selector.xpath("body/div[@class='u']/div[@class='tip2']")
        info_text = info.extract_first()
        try:
            item['ID'] = re.findall("uid=(.*?)\">", info_text)[0]
            item['TweetsNum'] = re.findall("微博\[(.*?)\]</span>", info_text)[0]
            item['FollowerNum'] = re.findall("关注\[(.*?)\]</span>", info_text)[0]
            item['FanNum'] = re.findall("粉丝\[(.*?)\]</span>", info_text)[0]
            tweet_url, follower_url = url_generator_for_id(item['ID'])
            item['URL'] = tweet_url
        except:
            pass
        basic_info_url = 'http://weibo.cn/%s/info' % item['ID']
        yield scrapy.Request(basic_info_url, meta={"item": item}, callback=self.parse_basic_info)

    def parse_basic_info(self, response):
        selector = scrapy.Selector(response)
        item = response.meta["item"]
        info_text = selector.xpath("body/div[6]").extract_first()
        info_dict = {'NickName': '昵称', 'Birthday': '生日', 'City': '地区', 'Gender': '性别', 'Marriage': '婚姻状况', 'Signature': '简介'}
        for each_item in info_dict:
            item[each_item] = find_basic_info(info_dict[each_item], info_text)
        yield item

