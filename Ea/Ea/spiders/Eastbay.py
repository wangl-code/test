import time

import scrapy

from Ea.items import EaItem


class EastbaySpider(scrapy.Spider):
    name = 'Eastbay'
    allowed_domains = ['eastbay.com']
    # start_urls = ['http://eastbay.com/']
    start_urls = ['https://www.eastbay.com/category/sale.html?query=sale%3Arelevance%3AstyleDiscountPercent%3ASALE%3Agender%3AMen%27s%3Abrand%3AASICS%20Tiger']

    def parse(self, response):
        nodes = response.xpath('//*[@id="main"]/div/div[2]/div/section/div/div[2]/ul/li')
        for node in nodes:
            parse_url_1 = node.xpath('./div/a/@href').extract_first()
            parse_url= 'https://www.eastbay.com'+ parse_url_1
            yield scrapy.Request(url=parse_url,
                                 # headers=headers,
                                 callback=self.pares_page,)
    def pares_page(self,response):
        items = EaItem()
        title = response.xpath('//*[@id="pageTitle"]/span[1]').extract_first()
        items['title'] = str(title).replace('<span itemprop="name" class="ProductName-primary">', '').replace('</span>', '')
        price = response.xpath('//*[@id="ProductDetails"]/div[4]/div[2]/span/span/span/span[2]').extract_first()
        items['price'] = str(price).replace('<span class="ProductPrice-final" aria-hidden="true">','').replace('</span>','')
        color = response.xpath('//*[@id="ProductDetails"]/div[4]/p[1]').extract_first()
        items['color'] = str(color).replace('<p class="ProductDetails-form__label" aria-live="polite">','').replace('</p>','')
        size = response.xpath('//*[@id="ProductDetails"]/div[4]/fieldset/div/div[@class="c-form-field c-form-field--radio ProductSize"]/label/span').extract()
        size_data = []
        for i in size:
            data = str(i).replace('<span class="c-form-label-content">','').replace('</span>','').strip().replace('\n','')
            size_data.append(data)
        items['size'] = size_data
        sku = response.xpath('//*[@id="ProductDetails-tabs-details-panel"]/text()').extract_first()
        items['sku'] = str(sku).replace('Product #: ','')
        details = response.xpath('//*[@id="ProductDetails-tabs-details-panel"]/div').extract_first()
        items['details'] = str(details).replace('<div class="ProductDetails-description">','').replace('<p>','').replace('</p>','').replace('<ul>','').replace('<li>','').replace('</li>','').replace('</ul>','').replace('</div>','').replace('<strong>','').replace('</strong>','').replace('<br>','\n')

        items['img_urls'] = 'https://images.footlocker.com/is/image/EBFL2/{}_a1?wid=541&hei=541&fmt=png-alpha'.format(items['sku'])
        # print(items)
        return items
