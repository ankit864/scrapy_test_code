#crawled and uploded
# -*- coding: utf-8 -*-

import scrapy
from functools import partial
import csv

class MybageechaSpider(scrapy.Spider):
    name = 'mybageecha'
    allowed_domains = ['mybageecha.com']
    start_urls = [
                    "https://mybageecha.com/collections/buy-planters-online"
                    "https://mybageecha.com/collections/buy-planters-online"
                    ]

    seller_id = 65169
    # category_id = raw_input("enter category_id")
    # sub_category  = raw_input("enter sub category ")

    def parse(self, response):
        urls = response.css('a[itemprop="url"]::attr(href)').extract()
        for url in urls:
            url = response.urljoin(url)
            print url
            yield scrapy.Request(url=url, callback=partial(self.parse_details,
                                            url=url,seller_id=self.seller_id,
                                            category_id=self.category_id,
                                            sub_category=self.sub_category))
            
        # follow pagination link
        next_page_url = response.css('span.next a::attr(href)').extract_first()
        print next_page_url
        if next_page_url:
            next_page_url = response.urljoin(next_page_url)
            yield scrapy.Request(url=next_page_url, callback=self.parse)
    
    #parsing details
    def parse_details(self, response,url = None,seller_id=None,category_id=None,sub_category=None):
            product_name = response.css('h1.product_name::text').extract_first()

            product_regular_price =  response.css('.eight.columns.omega .modal_price span[itemprop="price"] span::text').extract()
            product_regular_price = product_regular_price[0].strip()[3:].replace(',','')
            product_discounted_price = ""
            imgs = response.css("ul.slides li::attr(data-thumb)").extract()
            item = [ ]
            item.append(seller_id)
            item.append(category_id)
            item.append(sub_category)
            item.append(product_name)
            item.append(url)
            item.append(product_regular_price)
            item.append(product_discounted_price)
            img_count = 0
            for img in imgs:
                if img_count < 2:
                    img = "http:" + img
                    item.append(img)
                img_count = img_count + 1
            self.write_csv(item)

    def write_csv(self,item):
        f = open("mybageecha.csv", 'ab')
        w = csv.writer(f,dialect='excel',delimiter=',', quoting=csv.QUOTE_NONNUMERIC)
        main_list = []
        main_list.append(item)
        for item1 in main_list:
            print item1
            w.writerows([item1])
