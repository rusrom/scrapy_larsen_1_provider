# -*- coding: utf-8 -*-

from scrapy.http import Request
from scrapy.exceptions import DropItem
from scrapy.pipelines.images import ImagesPipeline


class HbarrysmithKaufmanauctionswvAuctionsfirstPipeline(object):
    def process_item(self, item, spider):
        return item


class LotImagesPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        return [Request(img_url, meta={'image_name': item['LotNum'], 'domain_folder': item['domain_folder'], 'auction_folder': item['auction_folder'], 'n': img_index}) for img_index, img_url in enumerate(item.get('image_urls', []), 1)]

    def file_path(self, request, response=None, info=None):
        return '{domain_folder}/{auction_folder}/{image_name}_{image_index}.jpg'.format(
            domain_folder=request.meta['domain_folder'],
            auction_folder=request.meta['auction_folder'],
            image_name=request.meta['image_name'],
            image_index=request.meta['n']
        )


class LotAdvertisePipeline(object):
    def process_item(self, item, spider):
        if item.get('LotNum').startswith('0'):
            raise DropItem('Lot with advertise information')
        return item
