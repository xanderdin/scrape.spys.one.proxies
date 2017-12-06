# -*- coding: utf-8 -*-

#
# Scrape all proxies from the first page of http://spys.one/proxies/
#

import scrapy
import re

from proxies.items import ProxiesItem


# Ports for proxies are encoded. Encoding table
# is present in the first <script> inside <body>.
# So we need to parse that script initially and
# decode values from javascripts which generate
# ports values for each proxy entry.
#
# Script with encoding table has two types of
# key=value entries.
#
# First type is plain, that is key=some_number.
# Plain type keys have always 4 symbols in length.
#
# Second type is calculated type. This type keys
# are alwasy 6 symbols in length.


# Encoding/decoding table
enctab = dict()


def fill_enctab(arg):
    '''
    Fill enctab with values from the script
    with encoding values.

    @arg - script body
    '''
    plain_values = [v for v in [x.split('=') for x in arg] if len(v[0]) == 4]
    for v in plain_values:
        enctab[v[0]] = int(v[1])
    other_values = [v for v in [x.split('=') for x in arg] if len(v[0]) == 6]
    for v in other_values:
        (a, b) = v[1].split('^')
        enctab[v[0]] = int(a) ^ enctab[b]


def calc_port(script):
    port = ''
    port_parts = re.findall('\+\(([a-z0-9^]+)\)+', script)
    for part in port_parts:
        (a, b) = part.split('^')
        port += str(enctab[a] ^ enctab[b])
    return port


class ProxiesSpider(scrapy.Spider):
    name = 'proxies'

    start_urls = [
        'http://spys.one/proxies/',
    ]

    def parse(self, response):

        # Get first body script with encoding table
        # and fill our enctab accordingly.
        script = response.xpath('//body/script[1]/text()').extract_first()
        fill_enctab(script.split(';'))

        # All rows which interest us have
        # 'onmouseover' attribute in common
        rows = response.css('tr[onmouseover]')
        for row in rows:
            item = ProxiesItem()
            # id = row.css('td:nth-child(1) font.spy1::text').extract_first()
            item['ip_address'] = row.css(
                'td:nth-child(1) font.spy14::text').extract_first()
            script = row.css(
                'td:nth-child(1) font.spy14 script::text').extract_first()
            item['port'] = calc_port(script)
            yield item
