# -*- coding: utf-8 -*-
import scrapy
import re

class AlkaramSpider(scrapy.Spider):
    name = 'alkaram'
    start_urls = ['https://www.alkaramstudio.com/unstitched','https://www.alkaramstudio.com/pret','https://www.alkaramstudio.com/kids/girls','https://www.alkaramstudio.com/kids/mak-girl','https://www.alkaramstudio.com/accessories/scarf']

    def parse(self, response):
        i=response.url
        cat_name={}
        if re.search("(?i)Unstitched", i) or re.search("(?i)Un-stitched", i):
            cat_name={"cat_name": "Unstitched"}
        elif re.search("(?i)scarf", i):
            cat_name={"cat_name": "Stole/Shawl"}
        elif re.search("(?i)Girl", i):
            cat_name={"cat_name": "KIDS"}
        elif re.search("(?i)Pret", i):
            cat_name={"cat_name": "IDEAS PRET"}

        yield scrapy.Request(i, callback=self.all_products, meta=cat_name)

    def all_products(self,response):

        prod_page_urls=response.xpath('//*[@class="item-inner"]/div/a/@href').extract()
        for url in prod_page_urls:
            yield scrapy.Request(url, callback=self.product_page, meta=response.meta)
        next_page=response.xpath('//*[@class="next i-next"]/@href').extract_first()
        if next_page!=None:
            yield scrapy.Request(next_page, callback=self.all_products, meta=response.meta)

    def product_page(self,response):
        converted_price=0
        img_url=response.xpath('//*[@id="cloudZoom"]/@href').extract_first()
        title=response.xpath('//*[@class="product-name"]/h1/text()').extract_first()
        price=response.xpath('//*[@class="regular-price"]/span/text()').extract_first()
        if price!=None:
            match = re.search(r'([\D]+)([\d,]+)',price)
            converted_price=int(match.group(2).replace(',',''))
        prod_page=response.url

        yield {"img_url":img_url,
               "title":title,
               "Price":converted_price,
               "prod_page":prod_page,
               'cat_name': response.meta['cat_name'],
               "Brand":"Alkaram Studio"

        }
