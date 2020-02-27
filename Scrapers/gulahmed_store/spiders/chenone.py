# -*- coding: utf-8 -*-
import scrapy
import re

class ChenoneSpider(scrapy.Spider):
    name = 'chenone'
    start_urls = ['https://www.chenone.com/women/stitched.html','https://www.chenone.com/women/bottom.html','https://www.chenone.com/women/tops.html','https://www.chenone.com/women/formal-suiting.html','https://www.chenone.com/women/active-wear.html','https://www.chenone.com/kids/girls.html']

    def parse(self, response):
        i=response.url
        cat_name={}
        if re.search("(?i)stitched", i) :
            cat_name={"cat_name": "STITCHED FABRIC"}
        elif re.search("(?i)bottom", i) or re.search("(?i)tops", i):
            cat_name={"cat_name": "SALT"}
        elif re.search("(?i)formal", i):
            cat_name={"cat_name": "IDEAS PRET"}
        elif re.search("(?i)active-wear", i):
            cat_name={"cat_name": "ACTIVE WEAR"}
        elif re.search("(?i)Girl", i):
            cat_name={"cat_name": "KIDS"}

        yield scrapy.Request(i, callback=self.all_products, meta=cat_name)

    def all_products(self,response):
        prod_page_urls=response.xpath('//*[@class="product-item-link"]/@href').extract()
        for url in prod_page_urls:
            yield scrapy.Request(url, callback=self.product_page, meta=response.meta)

        next_page=response.xpath('//*[@title="Next"]/@href').extract_first()
        if next_page!=None:
            yield scrapy.Request(next_page, callback=self.all_products, meta=response.meta)


    def product_page(self,response):
        converted_price=0
        img_url=response.xpath('//*[@class="MagicZoom"]/@href').extract_first()
        title=response.xpath('//*[@class="page-title"]/span/text()').extract_first()
        price=response.xpath('//*[@data-price-type="finalPrice"]/span/text()').extract_first()
        if price!=None:
            match= re.search(r'([\D]+)([\d,]+)',price)
            converted_price=int(match.group(2).replace(',',''))
        prod_page=response.url

        yield {"img_url":img_url,
               "title":title,
               "Price":converted_price,
               "prod_page":prod_page,
               'cat_name': response.meta['cat_name'],
               "Brand":"ChenOne"

        }
