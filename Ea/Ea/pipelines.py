# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import json

from itemadapter import ItemAdapter


class EaPipeline:
    def open_spider(self,spider):
        if spider.name == 'Eastbay':
            self.file = open('Eadata.json','w',encoding='utf-8')
        if spider.name == 'Zapp':
            self.file = open('Zadata.json','w',encoding='utf-8')
    def process_item(self, item, spider):
        # if spider.name == 'Eastbay':
        item = dict(item)
        str_data = json.dumps(item,ensure_ascii=False)+'\n'
        self.file.write(str_data)
        return item
    def close_spider(self,spider):
        # if spider.name == 'Eastbay':
        self.file.close()

