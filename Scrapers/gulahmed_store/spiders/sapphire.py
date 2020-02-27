# -*- coding: utf-8 -*-
import scrapy
import re

class SapphireSpider(scrapy.Spider):
    name = 'sapphire'
    start_urls = ['https://pk.sapphireonline.pk/collections/girls','https://pk.sapphireonline.pk/collections/active-wear','https://pk.sapphireonline.pk/collections/unstitched','https://pk.sapphireonline.pk/collections/formals','https://pk.sapphireonline.pk/collections/women-s-trousers','https://pk.sapphireonline.pk/collections/ready-to-wear']

    def parse(self, response):
        i=response.url
        cat_name={}
        if re.search("(?i)Unstitched", i) :
            cat_name={"cat_name": "Unstitched"}
        elif re.search("(?i)Girl", i):
            cat_name={"cat_name": "KIDS"}
        elif re.search("(?i)formal", i) or re.search("(?i)trousers", i) or re.search("(?i)Ready", i):
            cat_name={"cat_name": "IDEAS PRET"}
        elif re.search("(?i)active-wear", i):
            cat_name={"cat_name": "ACTIVE WEAR"}
        yield scrapy.Request(i, callback=self.all_products, meta=cat_name)

    def all_products(self,response):
        prod_page_urls=response.xpath('//*[@class="product-grid-image"]/@href').extract()
        for url in prod_page_urls:
            absolute_url=response.urljoin(url)
            yield scrapy.Request(absolute_url, callback=self.product_page, meta=response.meta)
        next_page=response.xpath('//*[@rel="next"]/@href').extract_first()
        if next_page!=None:
            absolute=response.urljoin(next_page)
            yield scrapy.Request(absolute, callback=self.all_products, meta=response.meta)


    def product_page(self,response):
        converted_price=0
        img_url=response.xpath('//*[@class="fancybox"]/@href').extract_first()
        title=response.xpath('//*[@class="product-title "]/h2/span/text()').extract_first()
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
               "Brand":"Sapphire"

        }

