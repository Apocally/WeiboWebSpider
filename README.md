# WeiboWebSpider
##运行环境：
python 3.6 [安装方法](http://www.cnblogs.com/hhh5460/p/5814275.html)
## 简介
1. 用 selenium+PhantomJS 模拟登录weibo.cn，获取cookies
2. scrapy 爬取新浪微博个人信息、微博信息
3. 保存到MongoDB
4. 验证码处理：人眼识别
  
为了防止账号被封，微博账号是淘宝买的，花了1块大洋，最后发现是直接封IP的。。。。

## 使用方法
1. 配置MongoDB，[启动](http://www.runoob.com/mongodb/mongodb-window-install.html)
2. CMD进入根目录（scrapy.cfg所在文件夹）
3. scrapy crawl WeiboWebSpider 或者 scrapy crawl WeiboWebSpider -s JOBDIR=crawls/WeiboWebSpider-1 [支持暂停](http://scrapy-chs.readthedocs.io/zh_CN/1.0/topics/jobs.html)
4. 注意Setting文件中的DownloadDelay，时间过短导致封IP，过一段时间恢复
