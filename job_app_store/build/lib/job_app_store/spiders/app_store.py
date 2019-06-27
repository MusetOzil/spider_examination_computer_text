# -*- coding: utf-8 -*-
import scrapy
from job_app_store.items import JobAppStoreItem,JobAndroidItem

class AppStoreSpider(scrapy.Spider):
    name = 'app_store'
    allowed_domains = ['chinaz.com']
    start_urls = ['https://aso.chinaz.com/']

    def parse(self, response):
        #appstore榜
        app_url = response.xpath('//ul[@class="header_nav"]/li[2]/a/@href').extract_first('')
        print(app_url)
        yield scrapy.Request(
            url=app_url,
            callback=self.parse_app_store
        )
        #安卓应用榜
        android_url = response.xpath('//ul[@class="header_nav"]/li[3]/a/@href').extract_first('')
        yield scrapy.Request(
            url=android_url,
            callback=self.parse_android_data
        )

    def parse_app_store(self,response):
        #获取app排行的列表
        app_data = response.xpath('//div[@class="table clear"]/ul/li')
        next_page_code =int(response.xpath('//ul[@class="pagination"]/li[last()-1]/a/text()').extract_first('').replace(' ',''))
        #循环遍历处理li内的数据
        for app in app_data:
            #获取app内容的详情url
            new_url=app.xpath('.//div[@class="table_intro"]/a/@href').extract_first('')
            #拿到URL后发起请求 回调到 parse_app 方法
            # print(new_url)
            yield scrapy.Request(
                url=new_url,
                callback=self.parse_app
            )
        # 获取最后一页的页码数
            for page in range(2,next_page_code+1):
                # print(page)
                #https://aso.chinaz.com/appstore.html?page=4
                #https://aso.chinaz.com/appstore.html?value=1&page=5
                #拼接下一页URL 发起请求
                next_page_url ='https://aso.chinaz.com/appstore.html?page=%s'%(str(page))
                yield scrapy.Request(
                    url=next_page_url,
                    callback=self.parse_app_store
                )


    def parse_app(self,response):
        # print('==================================================')
        # print(response.status)
        """
        # APP图片
        app_img = scrapy.Field()
        # 使用设备
        equipment = scrapy.Field()
        # 地区
        region = scrapy.Field()
        # 评论
        comment = scrapy.Field()
        # price价格
        price = scrapy.Field()
        # id号
        app_id = scrapy.Field()
        # 版本号
        id_code = scrapy.Field()
        # 开发商
        developers = scrapy.Field()
        # 总榜
        The_total_list = scrapy.Field()

        """
        #获取AppStore数据
        app_item = JobAppStoreItem()
        app_item['app_img'] = response.xpath('//div[@class="header_img"]/img/@src').extract_first('')
        app_item['equipment'] = response.xpath('//p[@class="js-down-up js-device"]/text()').extract_first('')
        app_item['region'] = response.xpath('//div[@class="header_table"]/div[2]//p[@class="js-down-up js-country"]/text()').extract_first('')
        app_item['comment'] = response.xpath('//div[@class="header_table"]/div[3]/p/text()').extract_first('')
        app_item['price'] = response.xpath('//div[@class="header_table"]/div[5]/div/text()').extract_first('').replace('\r','').replace('\n','').replace(' ','')
        app_item['app_id'] = response.xpath('//div[@id="jsAppId"]/a/text()').extract_first('').replace('\r','').replace('\n','').replace('','')
        app_item['id_code'] = response.xpath('//div[@class="header_table"]/div[7]/div/text()').extract_first('').replace('\r','').replace('\n','').replace(' ','')
        app_item['developers'] = response.xpath('//div[@class="header_table"]/div[8]/div/a/text()').extract_first('')
        app_item['The_total_list'] = response.xpath('//ul[@class="time_table"]/li[1]/span/text()').extract_first('')
        # print(app_item)
        yield app_item
    def parse_android_data(self,response):
        and_data = response.xpath('//div[@class="table clear"]/ul/li')
        next_page_code = int(
            response.xpath('//ul[@class="pagination"]/li[last()-1]/a/text()').extract_first('').replace(' ', ''))
        # 循环遍历处理li内的数据
        for app in and_data:
            # 获取app内容的详情url
            new_url = app.xpath('.//div[@class="table_intro"]/a/@href').extract_first('')
            # 拿到URL后发起请求 回调到 parse_app 方法
            # print(new_url)
            yield scrapy.Request(
                url=new_url,
                callback=self.parse_android
                )
            for page in range(2,next_page_code+1):
                # print(page)
                #拼接下一页URL 发起请求
                next_page_url ='https://aso.chinaz.com/android.html?value=2%s'%str(page)
                yield scrapy.Request(
                    url=next_page_url,
                    callback=self.parse_android_data
                )
    def parse_android(self,response):
        """
        # APP图片
        app_img = scrapy.Field()
        # 评论
        comment = scrapy.Field()
        # 版本号
        id_code = scrapy.Field()
        # 开发商
        developers = scrapy.Field()
        """
        android_item = JobAndroidItem()
        android_item['app_img'] = response.xpath('//div[@class="header_img"]/img/@src').extract_first('')
        android_item['comment'] = response.xpath('//div[@class="header_table"]/div[1]/p/text()').extract_first('')
        android_item['id_code'] = response.xpath('//div[@class="header_table"]/div[3]/div[2]/a/text()').extract_first('')
        android_item['developers'] = response.xpath('//div[@class="content cell_developer"]/text()').extract_first('').replace('\n','').replace(' ','').replace('\r','')
        android_item['paiming'] = response.xpath('//tbody[@class="rank_tbody"]/tr/td[3]/text()').extract_first('')
        # print(android_item)
        yield android_item

