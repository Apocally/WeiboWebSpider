import WeiboWebSpider.Login
from importlib import reload

myWeiBo = [
    {'no': '17057749219', 'psw': 'ws161208'},
    {'no': '15314789784', 'psw': 'ws161208'},
    {'no': '17133722284', 'psw': 'ws161208'}
]


def get_cookies_list():
    cookies_list = []
    while len(myWeiBo) is not 0:
        for each_item in myWeiBo:
            cookies, flag = WeiboWebSpider.Login.get_cookies(each_item['no'], each_item['psw'])
            if flag == 'succeeded':
                cookies_list.append(cookies)
                myWeiBo.pop(myWeiBo.index(each_item))
            reload(WeiboWebSpider.Login)
    return cookies_list
