# -*- coding: utf-8 -*-
import scrapy

from urllib.parse import urlsplit
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst
from hbarrysmith_kaufmanauctionswv_auctionsfirst.items import HbarrysmithKaufmanauctionswvAuctionsfirstItem


class HbsmithKaufmanswvAuctionfirstLotsSpider(scrapy.Spider):
    name = 'hbsmith_kaufmanswv_auctionfirst_lots'
    allowed_domains = ['hbarrysmith.com', 'kaufmanauctionswv.com', 'auctionsfirst.net', 'sheridanauctionservice.com']

    # https://bid.hbarrysmith.com/m/view-auctions/catalog/id/20733
    # https://bid.kaufmanauctionswv.com/m/view-auctions/catalog/id/20593/
    # https://bid.auctionsfirst.net/m/view-auctions/catalog/id/20838/

    custom_settings = {
        'FEED_EXPORT_FIELDS': ['LotNum', 'Lead', 'Description'],
        'IMAGES_STORE': '**********',
        'AWS_ACCESS_KEY_ID': '**********',
        'AWS_SECRET_ACCESS_KEY': '**********',
        'ITEM_PIPELINES': {
            'hbarrysmith_kaufmanauctionswv_auctionsfirst.pipelines.LotAdvertisePipeline': 10,
            'hbarrysmith_kaufmanauctionswv_auctionsfirst.pipelines.LotImagesPipeline': 100,
        },
    }

    def __init__(self, url, *args, **kwargs):
        super(HbsmithKaufmanswvAuctionfirstLotsSpider, self).__init__(*args, **kwargs)
        url_data = urlsplit(url)
        self.domain_name = url_data.hostname.split('.')[1]
        self.auction_id = url_data.path.rstrip('/').split('/')[-1]
        self.start_urls = [url + '?page=1&items=1200']

    def parse(self, response):
        lots = response.xpath('//li[contains(@id,"lot")]//h2/a')
        for lot in lots:
            yield response.follow(url=lot, callback=self.parse_lot)

    def parse_lot(self, response):
        l = ItemLoader(item=HbarrysmithKaufmanauctionswvAuctionsfirstItem(), response=response, blukit="sdfasdfasdfsa")
        l.default_output_processor = TakeFirst()

        l.add_xpath('LotNum', '//span[@class="lot-num"]/text()')
        l.add_xpath('Lead', '//span[@class="lot-name"]/text()')
        l.add_xpath('Description', 'string(//div[contains(@class, "description-info-content")])')
        l.add_xpath('image_urls', '//a[@data-fancybox-group]/@href')
        l.add_value('domain_folder', self.domain_name)
        l.add_value('auction_folder', self.auction_id)

        yield l.load_item()
