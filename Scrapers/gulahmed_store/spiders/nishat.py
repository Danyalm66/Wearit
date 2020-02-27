# -*- coding: utf-8 -*-
import scrapy
import re

class NishatSpider(scrapy.Spider):
    name = 'nishat'
    start_urls = ['http://nishatlinen.com/pk/women.html/']

    def parse(self, response):
        cat_urls= list(dict.fromkeys(response.xpath('//*[@class="level0 nav-1 first level-top parent"]/ul/li/a/@href').extract()))
        for i in cat_urls[1:]:
            if re.search("(?i)Unstitched", i):
                yield scrapy.Request(i, callback=self.all_products, meta={"cat_name": "Unstitched"})
            elif re.search("(?i)Ready", i) or re.search("(?i)fusion", i) or re.search("(?i)luxury", i):
                yield scrapy.Request(i, callback=self.all_products, meta={"cat_name": "STITCHED FABRIC"})
            elif re.search("(?i)lowers", i):
                yield scrapy.Request(i, callback=self.all_products, meta={"cat_name": "SALT"})
            elif re.search("(?i)ftb", i):
                yield scrapy.Request(i, callback=self.all_products, meta={"cat_name": "IDEAS PRET"})

    def all_products(self,response):
        prod_page_urls=response.xpath('//*[@class="product-item-link"]/@href').extract()
        for url in prod_page_urls:
            yield scrapy.Request(url, callback=self.product_page, meta=response.meta)
        next_page=response.xpath('//*[@class="action  next"]/@href').extract_first()
        if next_page!=None:
            yield scrapy.Request(next_page, callback=self.all_products, meta=response.meta)

    def product_page(self,response):
        converted_price=0
        img_url=response.xpath('//*[@class="MagicZoom"]/@href').extract_first()
        title=response.xpath('//*[@class="page-title"]/span/text()').extract_first()
        price=response.xpath('//*[@class="price-wrapper "]/span/text()').extract_first()
        if price!=None:
            match = re.search(r'([\D]+)([\d,]+)',price)
            converted_price=int(match.group(2).replace(',',''))
        prod_page=response.url

        yield {"img_url":img_url,
               "title":title,
               "Price":converted_price,
               "prod_page":prod_page,
               'cat_name': response.meta['cat_name'],
               "Brand":"Nishat Linen"

        }
