# -*- coding: utf-8 -*-
from urllib.parse import urlsplit

import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst

from hbarrysmith_kaufmanauctionswv_auctionsfirst.items import HbarrysmithKaufmanauctionswvAuctionsfirstResultItem


class HbsmithKaufmanswvAuctionfirstResultsSpider(scrapy.Spider):
    name = 'hbsmith_kaufmanswv_auctionfirst_results'
    allowed_domains = ['hbarrysmith.com', 'kaufmanauctionswv.com', 'auctionsfirst.net', 'sheridanauctionservice.com']

    # https://bid.hbarrysmith.com/m/view-auctions/catalog/id/20733
    # https://bid.kaufmanauctionswv.com/m/view-auctions/catalog/id/20593/
    # https://bid.auctionsfirst.net/m/view-auctions/catalog/id/20838/
    # https://bid.sheridanauctionservice.com/m/view-auctions/catalog/id/20650/

    custom_settings = {
        'FEED_EXPORT_FIELDS': ['LotNum', 'Lead', 'Description', 'Price', 'Sale'],
    }

    def __init__(self, url, *args, **kwargs):
        super(HbsmithKaufmanswvAuctionfirstResultsSpider, self).__init__(*args, **kwargs)
        url_data = urlsplit(url)
        self.domain_name = url_data.hostname.split('.')[1]
        self.auction_id = url_data.path.rstrip('/').split('/')[-1]
        self.start_urls = [url + '?page=1&items=1200']

    def parse(self, response):
        lots = response.xpath('//li[contains(@id,"lot") and .//div[@class="bdttle"]/i/a[not(starts-with(text(), 0))]]//h2/a')
        for lot in lots:
            yield response.follow(url=lot, callback=self.parse_lot)

    def parse_lot(self, response):
        l = ItemLoader(item=HbarrysmithKaufmanauctionswvAuctionsfirstResultItem(), response=response)
        l.default_output_processor = TakeFirst()

        l.add_xpath('LotNum', '//span[@class="lot-num"]/text()')
        l.add_xpath('Lead', '//span[@class="lot-name"]/text()')
        l.add_xpath('Description', 'string(//div[contains(@class, "description-info-content")])')
        l.add_xpath('Price', '//span[@id and contains(text(), "Lot closed - High bid:")]/span/text()')
        l.add_value('Sale', l.get_collected_values('Price'))

        yield l.load_item()
