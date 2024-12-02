import logging

import scrapy

logger = logging.getLogger(__name__)


class ThemoviedbSpider(scrapy.Spider):
    name = "TheMovieDB"
    allowed_domains = ["www.themoviedb.org"]
    start_urls = ["https://www.themoviedb.org/movie"]

    def parse(self, response):
        # logger.info(response.request.headers['User-Agent'])
        items = response.xpath(
            '//div[@class="media_items results"]//div[@class="content"]//a/@href'
        )
        yield from response.follow_all(items, callback=self.parse_item)

    def parse_item(self, reponse):
        # logger.info(response.request.headers['User-Agent'])
        yield {"item": reponse.url}
