# -*- coding: utf-8 -*-
import csv
from scrapy.exceptions import DropItem
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

# nltk.download('stopwords')


class FvisaPipeline(object):
    result_file = None
    writer = None
    keywords = ['major',
                'reject',
                'day',
                'week',
                'month',
                'year',
                'time',
                'approve',
                'approving',
                'accept'
                ]


    def open_spider(self, spider):
        self.result_file = open('results.csv', 'a',
                                newline='', encoding='utf-8')
        self.writer = csv.DictWriter(self.result_file,
                                     ["source_url", "keywords", "text"])

    def process_item(self, item, spider):
        item['text'] = str(item['text'].strip().replace('\n', '  '))

        #item['text'] = str(item['text'])
        #item['text'] = item['text'].strip().replace('\n', '  ')

        item_keywords = []
        for kw in self.keywords:
            if kw in item['text']:
                item_keywords.append(kw)
        if item_keywords:
            spider.log("Found a related entry!")
        else:
            raise DropItem('Not a relevant entry. Dropping...')
        item['keywords'] = ', '.join(item_keywords)


        self.writer.writerow(item)
        self.result_file.flush()

    def close_spider(self, spider):
        self.result_file.close()