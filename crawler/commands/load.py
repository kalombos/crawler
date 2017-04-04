# -*- coding: utf-8 -*-

from scrapy.commands import ScrapyCommand
from crawler.spiders.spider import Spider
from scrapy.exceptions import UsageError
from urllib.parse import urlsplit


class Command(ScrapyCommand):

    requires_project = True

    def syntax(self):
        return "[options] <url>"

    def short_desc(self):
        return 'Crawl website from url that you provided'

    def add_options(self, parser):
        super(Command, self).add_options(parser)
        parser.add_option(
            "-d", "--depth",
            type=int,
            help="The maximum depth that will be allowed to crawl for site"
        )

    def process_options(self, args, opts):
        super(Command, self).process_options(args, opts)
        if opts.depth is not None:
            self.settings.set('DEPTH_LIMIT', opts.depth)

    def run(self, args, opts):
        if len(args) != 1:
            raise UsageError()

        url = args[0]
        domain = urlsplit(url).netloc
        Spider.domain = domain
        Spider.allowed_domains = [Spider.domain]
        Spider.start_urls = [url]
        self.crawler_process.crawl(Spider)
        self.crawler_process.start()
