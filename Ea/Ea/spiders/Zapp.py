import scrapy


class ZappSpider(scrapy.Spider):
    name = 'Zapp'
    allowed_domains = ['zappos.com']
    start_urls = ['https://www.zappos.com/men-sneakers-athletic-shoes/CK_XARC81wHAAQLiAgMBAhg.zso']

    def parse(self, response):
        nodes = response.xpath('//*[@id="products"]/article')
        print(len(nodes))
        for node in nodes:
            parse_url_1 = node.xpath('./a/@href').extract_first()
            parse_url = 'https://www.zappos.com/'+ parse_url_1
            # print(parse_url)

        pass
