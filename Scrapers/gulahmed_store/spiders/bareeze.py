# -*- coding: utf-8 -*-
import scrapy
import re

class BareezeSpider(scrapy.Spider):
    name = 'bareeze'
    start_urls = ['https://www.bareeze.com/pk/pants.html','https://www.bareeze.com/pk/fabric/casual.html','https://www.bareeze.com/pk/fabric/formal.html','https://www.bareeze.com/pk/fabric/winter-fabric/shawls.html']

    def parse(self, response):
        i=response.url
        cat_name={}
        if re.search("(?i)casual", i) :
            cat_name={"cat_name": "Unstitched"}
        elif re.search("(?i)formal", i):
            cat_name={"cat_name": "IDEAS PRET"}
        elif re.search("(?i)shawls", i):
            cat_name={"cat_name": "Stole/Shawl"}
        elif re.search("(?i)pants", i):
            cat_name={"cat_name": "SALT"}


        yield scrapy.Request(i, callback=self.all_products, meta=cat_name)

    def all_products(self,response):
        prod_page_urls=response.xpath('//*[@class="product-name"]/a/@href').extract()
        for url in prod_page_urls:
            yield scrapy.Request(url, callback=self.product_page, meta=response.meta)
        next_page=response.xpath('//*[@class="next i-next"]/@href').extract_first()
        if next_page!=None:
            yield scrapy.Request(next_page, callback=self.all_products, meta=response.meta)

    def product_page(self,response):
        converted_price=0
        img_url=response.xpath('//*[@class="MagicZoom"]/@href').extract_first()
        title=response.xpath('//*[@class="product-name"]/span/text()').extract_first()
        price=response.xpath('//*[@class="regular-price"]/span/text()').extract_first()
        if price!=None:
            converted_price=int(int(price.replace(',','')))
        prod_page=response.url

        yield {"img_url":img_url,
               "title":title,
               "Price":converted_price,
               "prod_page":prod_page,
               'cat_name': response.meta['cat_name'],
               "Brand":"Bareeze"

        }
