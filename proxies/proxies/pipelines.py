# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.exceptions import DropItem
from .database import Proxy, session


class ProxiesPipeline(object):
    def process_item(self, item, spider):
        if item['ip_address'] and item['port']:
            entry = session.query(Proxy).filter_by(
                ip_address=item['ip_address'],
                port=item['port']
            ).first()
            if entry:
                raise DropItem("Duplicate item found: %s" % item)
        entry = Proxy(**item)
        session.add(entry)
        session.commit()
        return item
