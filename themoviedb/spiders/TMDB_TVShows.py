import logging

import scrapy

logger = logging.getLogger(__name__)


class TmdbTvshowsSpider(scrapy.Spider):
    name = "TMDB_TVShows"
    allowed_domains = ["www.themoviedb.org"]
    start_urls = ["https://www.themoviedb.org/tv"]

    pagination_count = 0

    def parse(self, response):
        logger.info(response.url)
        self.pagination_count += 1
        tvshow_items = response.xpath(
            '//div[@class="media_items results"]//div[@class="content"]//a/@href'
        )
        yield from response.follow_all(tvshow_items, callback=self.parse_tvshow)

    def parse_tvshow(self, response):
        url = response.url
        title = response.xpath('//div[@class="title ott_false"]/h2/a/text()').get()
        publish_year = response.xpath('//div[@class="title ott_false"]/h2//span/text()').get()
        certification = response.xpath(
            '//div[@class="title ott_false"]/div[@class="facts"]/span[@class="certification"]/text()'
        ).get()
        genres = response.xpath(
            '//div[@class="title ott_false"]/div[@class="facts"]/span[@class="genres"]//text()'
        ).getall()
        user_score = response.xpath('//div[@class="user_score_chart"]/@data-percent').get()
        header_info = response.xpath('//div[@class="header_info"]/h3/text()').get()
        overview = response.xpath(
            '//div[@class="header_info"]/div[@class="overview"]/p/text()'
        ).get()
        top_billed_cast = response.xpath(
            '//div[@id="cast_scroller"]/ol[@class="people scroller"]/li/p/a/text()'
        ).getall()
        keywords = response.xpath(
            '//section[@class="keywords right_column"]//a[@class="rounded" or @class="!border !border-tmdb-light-blue font-semibold"]/text()'
        ).getall()
        tvshow_item = {
            "url": url,
            "title": title,
            "publish_year": publish_year,
            "certification": certification,
            "genres": genres,
            "user_score": user_score,
            "header_info": header_info,
            "overview": overview,
            "top_billed_cast": top_billed_cast,
            "keywords": keywords,
        }
        yield tvshow_item
