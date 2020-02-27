# -*- coding: utf-8 -*-
import scrapy
import re

class GulahmedSpider(scrapy.Spider):
    name = 'gulahmed'
    start_urls = ['https://www.gulahmedshop.com/women/']

    def parse(self, response):
        categories_urls= response.xpath('/html/body/div[1]/header/div[2]/div[3]/div/div[1]/div/div/div[2]/div/div/div/div/ul/li[3]/ul/li/div/div/div/p[@class="groupdrop-title"]/a')
        for category in categories_urls:
            products=category.xpath('./@href').extract_first()
            category_name=category.xpath('./text()').extract_first().strip()
            yield scrapy.Request(products, callback=self.all_products, meta={'Category Name':category_name})
        for i in response.xpath('//*[@class="menu-link"]/@href').extract():
            if re.search("(?i)Unstitched", i):
                yield scrapy.Request(i, callback=self.all_products, meta={'Category Name':"Unstitched"})

    def all_products(self, response):
        product_urls=response.xpath('//*[@class="cdz-product-top"]/a/@href').extract()
        for url in product_urls:
            yield scrapy.Request(url, callback=self.product_page, meta={'Category Name': response.meta['Category Name']})
        next_page_url=response.xpath('//*[@title="Next"]/@href').extract_first()
        if next_page_url!=None:
            yield scrapy.Request(next_page_url, callback=self.all_products,  meta={'Category Name': response.meta['Category Name']})
    def product_page(self,response):
        image=response.xpath('//*[@class="MagicZoom"]/@href').extract_first()
        product_title=response.xpath('//*[@class="page-title"]/span/text()').extract_first()
        price=response.xpath('//*[@data-price-type="finalPrice"]/span/text()').extract_first()
        converted_price=0
        if price!=None:
            match= re.search(r'([\D]+)([\d,]+)',price)
            converted_price=int(match.group(2).replace(',',''))
        page_url=response.url
        yield {'img_url':image,
               'title':product_title,
               'Price':converted_price,
               'prod_page': page_url,
               'cat_name': response.meta['Category Name'],
               'Brand':'Gul Ahmed'
        }



