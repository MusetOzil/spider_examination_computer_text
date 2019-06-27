# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql

class JobAppStorePipeline(object):
    def __init__(self, host, user, password, port, database, charset):
            # 创建数据库链接
            self.client = pymysql.Connect(
                host=host, user=user,
                password=password, database=database,
                port=port, charset=charset
            )
            # 创建游标
            self.mycursor = self.client.cursor()

    @classmethod
    def from_crawler(cls, crawler):
        host = crawler.settings['MYSQL_HOST']
        user = crawler.settings['MYSQL_USER']
        password = crawler.settings['MYSQL_PASSWORD']
        port = crawler.settings['MYSQL_PORT']
        database = crawler.settings['MYSQL_DATABASE']
        charset = crawler.settings['MYSQL_CHARSET']
        return cls(host, user, password, port, database, charset)

    def process_item(self, item, spider):
        item_dict = dict(item)
        sql_insert, values = item.get_sql_str(item_dict)
        try:
            self.mycursor.execute(sql_insert, values)
            self.client.commit()
        except Exception as err:
            print(err)
            self.client.rollback()
        return item

    def close_spider(self, spider):
        self.client.close()
        self.mycursor.close()
        print('爬虫结束')
