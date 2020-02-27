# -*- coding: utf-8 -*-
import scrapy
import logging
import re
class KhaadiSpider(scrapy.Spider):
    name = 'khaadi'
    start_urls = ['https://www.khaadi.com/pk']

    def parse(self, response):
        categories=[]
        ready_to_wear=response.xpath('//*[@class="level0 nav-2 category-item level-top parent"]/div/ul/li/a/@href').extract()
        kids=response.xpath('//*[@class="level0 nav-3 category-item level-top parent"]/div/ul/li/a/@href').extract()
        unstiched=response.xpath('//*[@class="level0 nav-1 category-item first level-top parent"]/a/@href').extract_first()
        categories=ready_to_wear+kids
        categories.append(unstiched)
        categories=list(dict.fromkeys(categories))
        for i in categories:
            if re.search("(?i)Unstitched", i):
                yield scrapy.Request(i, callback=self.all_products, meta={"cat_name": "Unstitched"})
            elif re.search("(?i)Ready", i):
                if re.search("(?i)Pret", i):
                    yield scrapy.Request(i, callback=self.all_products, meta={"cat_name": "IDEAS PRET"})
                elif re.search("(?i)Khaas", i):
                    yield scrapy.Request(i, callback=self.all_products, meta={"cat_name": "IDEAS PRET"})
                elif re.search("(?i)Bottoms", i):
                    yield scrapy.Request(i, callback=self.all_products, meta={"cat_name": "SALT"})
            elif re.search("(?i)Kids", i):
                if re.search("(?i)Girl", i):
                    yield scrapy.Request(i, callback=self.all_products, meta={"cat_name": "KIDS"})

    def all_products(self,response):

        urls= response.xpath('//*[@class="product-item-info"]/a/@href').extract()
        for url in urls:
            yield scrapy.Request(url, callback=self.product_page,meta={'cat_name': response.meta['cat_name']})
        next_page=response.xpath('//*[@class="action  next"]/@href').extract_first()
        if next_page!=None:
            yield scrapy.Request(next_page, callback=self.all_products, meta={'cat_name': response.meta['cat_name']})
        logging.info("Scraped all the pages Successfuly....")

    def product_page(self,response):
        converted_price=0
        img_url= response.xpath('//*[@class="MagicZoom"]/@href').extract_first()
        title= response.xpath('//*[@class="page-title"]/span/text()').extract_first()
        price=response.xpath('//*[@data-price-type="finalPrice"]/span/text()').extract_first()
        if price!=None:
            match = re.search(r'([\D]+)([\d,]+)',price)
            converted_price=int(match.group(2).replace(',',''))
        prod_page=response.url

        yield {"img_url":img_url,
               "title":title,
               "Price":converted_price,
               "prod_page":prod_page,
               'cat_name': response.meta['cat_name'],
               "Brand":"Khaadi"

        }
