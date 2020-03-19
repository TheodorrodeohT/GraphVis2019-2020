# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import re
from scrapy import Item, Field
from scrapy.loader.processors import TakeFirst, MapCompose, Join

def format(value):
    return value.strip()

def format_date(value):
    return re.sub('\(|\)', '', value)

def format_cast(value):
    if not re.findall('See full', value):
        return value

class Movie(Item):
    title               = Field(output_processor=TakeFirst(),   input_processor=MapCompose(format))
    release_date        = Field(output_processor=TakeFirst(),   input_processor=MapCompose(format, format_date))
    director            = Field(output_processor=TakeFirst())
    cast_top3           = Field(output_processor=Join(','),     input_processor=MapCompose(format_cast))
    runtime             = Field(output_processor=TakeFirst(),   input_processor=MapCompose(format))
    imdb_rating         = Field(output_processor=TakeFirst())
    genres              = Field(output_processor=Join(', '),    input_processor=MapCompose(format))
    budget              = Field(output_processor=TakeFirst(),   input_processor=MapCompose(format))
    language            = Field(output_processor=TakeFirst())