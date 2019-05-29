# -*- coding: utf-8 -*-
import scrapy
import nltk 
from nltk.stem import PorterStemmer
from fvisa.items import FvisaItem

stop_words = nltk.corpus.stopwords.words('english') + [
    '.',',','--','\'s','?',')','(',':','\'','\'re','"',"-",'}','{',u'-','\r','\n','\t',
    ]

ps = PorterStemmer()

class MainSpider(scrapy.Spider):
    name = 'main'
    allowed_domains = ['www.immihelp.com']

    def start_requests(self):
        for i in range(1, 529):
            url = 'https://www.immihelp.com/forum/usa-student-visa/page' + str(i)
            yield scrapy.Request(url=url, callback=self.parse)

    def parse_detail_page(self, response):
        texts = response.css('div.js-post__content-text::text').getall()
        for text in texts:

            tokens = nltk.word_tokenize(text) 
            words_ns = []
            for word in tokens:
                
                if word not in stop_words:
                    words_ns.append(ps.stem(word.lower()))

            sentence = ' '.join(map(str, words_ns)) 
            #print(sentence)

            yield FvisaItem(source_url=response.url, text=sentence)

    def parse(self, response):
        urls = response.css('a.topic-title.js-topic-title::attr(href)').getall()
        for url in urls:
            yield scrapy.Request(url, callback=self.parse_detail_page)
