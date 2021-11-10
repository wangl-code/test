import re

import scrapy

from Ea.items import EaItem


class ZappSpider(scrapy.Spider):
    name = 'Zapp'
    allowed_domains = ['zappos.com']
    start_urls = ['https://www.zappos.com/men-sneakers-athletic-shoes/CK_XARC81wHAAQLiAgMBAhg.zso']

    def parse(self, response):
        nodes = response.xpath('//*[@id="products"]/article')
        print(len(nodes))
        for node in nodes:
            item = EaItem()
            parse_url_1 = node.xpath('./a/@href').extract_first()
            parse_url = 'https://www.zappos.com/'+ parse_url_1
            item['parse_url'] = parse_url
            yield scrapy.Request(url=parse_url,callback=self.parse_page,meta={'item':item})
    def parse_page(self,response):
        items = response.meta['item']
        title = response.xpath('/html/head/title').extract_first()
        items['title'] = str(title).replace('<title>','').replace(' | Zappos.com</title>','')
        price = response.xpath('//*[@id="productRecap"]/div[1]/div[2]/div/div[1]/div[1]/div/span/span').extract_first()
        items['price'] = str(price).replace('<span aria-hidden="true"><span class="iz-z','').replace('itemprop="priceCurrency" content="USD">','').replace('</span>','').replace('<span class="kz-z">','').replace('</span><span class="jz-z">','').replace('</span></span>','').replace('<span class="jz-z">','')
        color = response.xpath('//*[@id="buyBoxForm"]/div[1]/div//text()').extract()
        items['color'] = color
        size = response.xpath('//*[@id="pdp-size-select"]//text()').extract()
        items['size'] = size
        items['sku'] = response.xpath('//*[@id="breadcrumbs"]/div[2]/span/text()').extract_first()
        items['details'] = response.xpath('//*[@id="productRecap"]/div[4]/div/div/div[2]/ul/li//text()').extract()
        if len(items['details']) == 0:
            items['details'] = response.xpath('//*[@id="productRecap"]/div[5]/div/div/div[2]/ul/li//text()').extract()
            items['img_urls'] = response.xpath('//*[@id="productImages"]/div[2]/div/div/div/div/button/img/@srcset').extract_first()
        # with open("data.html",'w',encoding='utf-8') as f:
        #     f.write(response.text)
        # print(item)
        return items
