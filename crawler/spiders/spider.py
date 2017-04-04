# -*- coding: utf-8 -*-
from scrapy.spiders import CrawlSpider, Rule
from crawler.items import PageItem
from scrapy.linkextractors import LinkExtractor


class Spider(CrawlSpider):
    name = "spider"
    domain = None

    rules = (
        Rule(LinkExtractor(), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        item = PageItem()
        titles = response.xpath('//title/text()').extract()
        if titles:
            item['url'] = response.url
            item['title'] = titles[0]
            yield item
