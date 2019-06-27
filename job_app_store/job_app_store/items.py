# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class JobAppStoreItem(scrapy.Item):
    #APP图片
    app_img = scrapy.Field()
    #使用设备
    equipment = scrapy.Field()
    #地区
    region = scrapy.Field()
    #评论
    comment= scrapy.Field()
    #price价格
    price = scrapy.Field()
    #id号
    app_id =scrapy.Field()
    #版本号
    id_code = scrapy.Field()
    #开发商
    developers = scrapy.Field()
    #总榜
    The_total_list = scrapy.Field()
    def get_sql_str(self, data):
        sql_insert = """
                INSERT INTO %s (%s)
                VALUES (%s)
                """ % (
            'appstore',
            ','.join(data.keys()),
            ','.join(['%s'] * len(data))
        )
        values = list(data.values())
        return sql_insert, values

    def get_collection_name(self):
        return 'appstore'
class JobAndroidItem(scrapy.Item):
    # APP图片
    app_img = scrapy.Field()
    # 评论
    comment = scrapy.Field()
    # 版本号
    id_code = scrapy.Field()
    # 开发商
    developers = scrapy.Field()
    #排名
    paiming = scrapy.Field()
    def get_sql_str(self, data):
        sql_insert = """
                INSERT INTO %s (%s)
                VALUES (%s)
                """ % (
            'android_table',
            ','.join(data.keys()),
            ','.join(['%s'] * len(data))
        )
        values = list(data.values())
        return sql_insert, values

    def get_collection_name(self):
        return 'android_table'