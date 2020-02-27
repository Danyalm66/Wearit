# -*- coding: utf-8 -*-
import scrapy
import re

class BonanzaSpider(scrapy.Spider):
    name = 'bonanza'
    start_urls = ['https://www.bonanzasatrangi.com/pk/unstitched/','https://www.bonanzasatrangi.com/pk/pret/','https://www.bonanzasatrangi.com/pk/kids/','https://www.bonanzasatrangi.com/pk/accessories/dupatta/','https://www.bonanzasatrangi.com/pk/accessories/shalwar/','https://www.bonanzasatrangi.com/pk/accessories/trouser/','https://www.bonanzasatrangi.com/pk/accessories/jeggings/']

    def parse(self, response):
        i=response.url
        cat_name={}
        if re.search("(?i)Unstitched", i):
            cat_name={"cat_name": "Unstitched"}
        elif re.search("(?i)Pret", i):
            cat_name={"cat_name": "IDEAS PRET"}
        elif re.search("(?i)kid", i):
            cat_name={"cat_name": "KIDS"}
        elif re.search("(?i)dupatta", i):
            cat_name={"cat_name": "Stole/Shawl"}
        elif re.search("(?i)shalwar", i) or re.search("(?i)trouser", i) or re.search("(?i)jeggings", i):
            cat_name={"cat_name": "SALT"}
        yield scrapy.Request(i, callback=self.all_products, meta=cat_name)

    def all_products(self,response):
        prod_page_urls=response.xpath('//*[@class="product-name"]/a/@href').extract()
        for url in prod_page_urls:
            yield scrapy.Request(url, callback=self.product_page, meta=response.meta)
        next_page=response.xpath('//*[@class="action  next"]/@href').extract_first()
        if next_page!=None:
            yield scrapy.Request(next_page, callback=self.all_products, meta=response.meta)


    def product_page(self,response):
        converted_price=0
        img_url=response.xpath('//*[@class="MagicZoom"]/@href').extract_first()
        title=response.xpath('//*[@class="product-name"]/span/text()').extract_first()
        price=response.xpath('//*[@itemprop="price"]/span/text()').extract_first()
        if price!=None:
            match = re.search(r'([\D]+)([\d,]+)',price)
            converted_price=int(match.group(2).replace(',',''))
        prod_page=response.url

        yield {"img_url":img_url,
               "title":title,
               "Price":converted_price,
               "prod_page":prod_page,
               'cat_name': response.meta['cat_name'],
               "Brand":"Bonanza Satrangi"

        }
