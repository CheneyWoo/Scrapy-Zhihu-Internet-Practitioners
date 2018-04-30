# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
'''
from scrapy.conf import settings
import pymysql
import MySQLdb

class ZhihuUserPipeline(object):

    def __init__(self, dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls, settings):
        dbparams = dict(
            host=settings['MYSQL_HOST'],
            db=settings['MYSQL_DBNAME'],
            user=settings['MYSQL_USER'],
            passwd=settings['MYSQL_PASSWD'],
            charset='utf8',  # 编码要加上，否则可能出现中文乱码问题
            cursorclass=MySQLdb.cursors.DictCursor,
            use_unicode=False,
        )
        dbpool = adbapi.ConnectionPool('MySQLdb', **dbparams)
        return cls(dbpool)

    def process_item(self, item, spider):
        query = self.dbpool.runInteraction(self._conditional_insert, item)
        query.addErrback(self._handle_error, item, spider)
        return item

    def _conditional_insert(self, tx, item):
        sql = "insert into zhihu_users(id,name,account_status,business,employments,description,educations,headline,locations,type,url,url_token,user_type) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        params = (
        item['id'], item['name'], item['account_status'], item['business'], item['employments'], item['description'], item['educations'],
        item['headline'], item['locations'], item['type'], item['url'], item['url_token'], item['user_type'])
        tx.execute(sql, params)

    def _handle_error(self, failue, item, spider):
        print failue
'''
import json
from scrapy.conf import settings
import codecs

class ZhihuUserPipeline(object):
    #def __init__(self):
    #    self.file = open('zhihu.csv', 'a+')

    def process_item(self, item, spider):
        line = json.dumps(dict(item), ensure_ascii=False) + "\n"
        temp = line.encode("utf-8")
        #print(temp)
        #mylist = temp.split(",")
        mydict = eval(temp)
        #print("我想在这里知道类型")
        #print(type(mydict))
        #print(mydict.keys())
        with open("zhihu.csv", 'a+') as file:
            '''
            for key in mydict.keys():
                if key == 'description':
                    print(mydict[key])
                    file.write(mydict[key])
                    file.write("\t")
            '''
            for key in mydict.keys():
                if key == 'business':
                    file.write("\n")
                    print(mydict[key]['name'])
                    file.write(mydict[key]['name'])
                    file.write("\t")
            for key in mydict.keys():
                if key == 'employments':
                    print(mydict[key][0]['job']['name'])
                    file.write(mydict[key][0]['job']['name'])
            file.write("\t,")
            for key in mydict.keys():
                if key == 'locations':
                    print(mydict[key][0]['name'])
                    file.write(mydict[key][0]['name'])
                    file.write("\n")
        #self.file.write(line.keys())
        return item
    def spider_closed(self, spider):
        self.file.close()