# -*- coding: utf-8 -*-

from scrapy.commands import ScrapyCommand
from scrapy.exceptions import UsageError
from urllib.parse import urlsplit
import pymongo


class Command(ScrapyCommand):

    default_settings = {'LOG_ENABLED': False}
    requires_project = True

    def syntax(self):
        return "<url>"

    def short_desc(self):
        return 'Get scraped pages from storage'

    def add_options(self, parser):
        super(Command, self).add_options(parser)
        parser.add_option(
            "-n", '--limit',
            type=int,
            default=50,
            help="Limit for count of records"
        )

    def run(self, args, opts):

        if len(args) != 1:
            raise UsageError()

        url = args[0]
        domain = urlsplit(url).netloc

        mongo_uri = self.crawler_process.settings.get('MONGO_URI')
        mongo_db = self.crawler_process.settings.get('MONGO_DATABASE')
        client = pymongo.MongoClient(mongo_uri)
        db = client[mongo_db]
        query = db.pages.find({'domain': domain}).limit(opts.limit)\
            .sort('date', -1)
        for rec in query:
            print('%s: "%s"' % (rec['url'], rec['title']))
        client.close()
