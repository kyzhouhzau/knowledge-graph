# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import os
import csv
import pymysql.cursors
import pymysql
class Pipline_ToCSV(object):
    def __init__(self):
        basepath = os.path.split(os.path.realpath(__file__))[0]
        store_file = os.path.join(basepath,"data/result.csv")
        self.file = open(store_file,'a')
        self.writer = csv.writer(self.file, delimiter=',')

    def process_item(self,item,spider):
        rows = item["MIM"],item["gene"],item["mutation"],item["disease"],item["article"]
        self.writer.writerow(rows)
        return item

    def close_spider(self,spider):
        self.file.close()

class MySQl_Save(object):
    def __init__(self,connect,cursor):
        self.connect = connect
        self.cursor = cursor

    @classmethod
    def from_settings(cls,settings):
        connect = pymysql.connect(
            host=settings['MYSQL_HOST'],
            db=settings['MYSQL_DBNAME'],
            port=settings['PORT'],
            user=settings['MYSQL_USER'],
            passwd=settings['MYSQL_PASSWD'],
            charset='utf8',
            use_unicode=False,
        )
        cursor = connect.cursor()
        return cls(connect,cursor)

    def process_item(self,item,spider):
        self.cursor.execute("""INSERT INTO kg_data(MIM,GENE,MUTATION,DISEASE,TEXT)
        VALUE (%s,%s,%s,%s,%s);""", (item["MIM"],item["gene"],item["mutation"],
                                    item["disease"],item["article"]))
        self.connect.commit()
        return item







