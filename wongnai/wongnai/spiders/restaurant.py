# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class RestaurantSpider(CrawlSpider):
    name = 'restaurant'
    allowed_domains = ['wongnai.com']

    user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36'

    def start_requests(self):
        yield scrapy.Request(url='https://www.wongnai.com/restaurants?categories=59&regions=9681', headers={
            'User-Agent': self.user_agent
        })

    rules = (
        Rule(LinkExtractor(restrict_xpaths="//div[contains(@class, 'do39q0-0 fxQZvy')]/a"), callback='parse_item', follow=True, process_request='set_user_agent'),
        Rule(LinkExtractor(restrict_xpaths="(//a[contains(@class, 'k0pvs2-0 gciMDQ')])"), process_request='set_user_agent'),
        Rule(LinkExtractor(restrict_xpaths="//div[contains(@class, 'sc-1365huc-0 lmzPAI y13xht-0 uts45i-0 jjGpck')]/div[2]/a"), callback = 'parse_product_item', follow = True, process_request = 'set_user_agent')
    )

    def set_user_agent(self, request):
        request.headers['User-Agent'] = self.user_agent
        return request

    def parse_item(self, response):
        yield {
            "cafe_name": response.xpath("//h1[contains(@class, 'sc-1iyq3yo-1 NbQyr')]/a/text()").get(),
            "cafe_category": response.xpath("//span[contains(@class, 'sc-1a3arn4-3 dVdRMK')]/a/text()").get(),
            "product_photos": response.xpath("//div[contains(@class, 'sc-1dtmzcy-1 hNLvuX')]/img/@src").get()
        }

    def parse_product_item(self, response):
        yield{
            "product_name": response.xpath("//div[contains(@class, 'ricb8s-2 gySlrN')]/div/text()").get(),
            "product_price": response.xpath("//div[contains(@class, 'ricb8s-6 dmTbmp')]/div/text()").get(),
            "product_image": response.xpath("//div[contains(@class, '_21btc6ycbuwmnmRpkhCZGl')]/div/img/@src").get(),
            "product_recommended_by_user": response.xpath("//div[contains(@class, 'mnqwk5-0 iZxyeW')]/div/a/div/img/@src").get()
        }

