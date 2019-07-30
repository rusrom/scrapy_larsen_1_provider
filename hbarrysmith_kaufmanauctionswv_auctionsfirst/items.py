# -*- coding: utf-8 -*-

import scrapy
import re

from w3lib.html import replace_escape_chars, replace_entities
from scrapy.loader.processors import Identity, MapCompose, Join, Compose


def absolute_url(url, loader_context):
    return loader_context['response'].urljoin(url)


def remove_garbage(val):
    val = re.sub(r'\s{2,}', ' ', val)
    val = re.sub(r'\s+,\s{1,}', ', ', val)
    val = replace_escape_chars(val)
    val = replace_entities(val)
    return val.strip()


def get_price(val):
    price = val.replace('$', '')
    price = price.replace(',', '')
    price = price.strip()
    return price


class HbarrysmithKaufmanauctionswvAuctionsfirstItem(scrapy.Item):
    LotNum = scrapy.Field(
        input_processor=MapCompose(
            lambda val: val.strip(),
        )
    )
    Lead = scrapy.Field()
    Description = scrapy.Field(
        input_processor=MapCompose(
            remove_garbage,
        )
    )
    image_urls = scrapy.Field(
        input_processor=MapCompose(
            absolute_url,
        ),
        output_processor=Identity(),
    )
    images = scrapy.Field()
    domain_folder = scrapy.Field()
    auction_folder = scrapy.Field()


class HbarrysmithKaufmanauctionswvAuctionsfirstResultItem(scrapy.Item):
    LotNum = scrapy.Field(
        input_processor=MapCompose(
            lambda val: val.strip(),
        )
    )
    Lead = scrapy.Field()
    Description = scrapy.Field(
        input_processor=MapCompose(
            remove_garbage,
        )
    )
    Price = scrapy.Field(
        input_processor=Compose(
            lambda val: [get_price(val[0])] if val else ['Unsold'],
        )
    )
    Sale = scrapy.Field(
        input_processor=MapCompose(
            lambda val: 'Yes' if 'Unsold' not in val else 'No',
        )
    )
