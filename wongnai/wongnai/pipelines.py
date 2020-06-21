# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import sqlite3
import logging


class WongnaiPipeline(object):
    def open_spider(self, spider):
        self.connection = sqlite3.connect("restaurant.db")
        self.c = self.connection.cursor()
        try:
            self.c.execute('''
                CREATE TABLE restaurant(
                cafe_name TEXT,
                cafe_category TEXT,
                product_photos TEXT,
                product_name TEXT,
                product_price TEXT,
                product_image TEXT,
                product_recommended_by_user TEXT
                )
            ''')
            self.connection.commit()
        except sqlite3.OperationalError:
            pass

    def close_spider(self, spider):
        self.connection.close()

    def process_item(self, item, spider):
        self.c.execute('''
            INSERT INTO restaurant(cafe_name, cafe_category, product_photos, product_name, product_price, product_image, product_recommended_by_user) values (?,?,?,?,?,?,?)
        ''', (
            item.get('cafe_name'),
            item.get('cafe_category'),
            item.get('product_photos'),
            item.get('product_name'),
            item.get('product_price'),
            item.get('product_image'),
            item.get('product_recommended_by_user')
        ))
        self.connection.commit()
        return item