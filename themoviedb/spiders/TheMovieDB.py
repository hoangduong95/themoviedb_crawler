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

    def parse_item(self, response):

        url = response.url
        title = response.xpath('//div[@class="title ott_false"]/h2/a/text()').get()
        publish_year = response.xpath('//div[@class="title ott_false"]/h2/span/text()').get()
        certification = (
            response.xpath(
                '//div[@class="title ott_false"]/div[@class="facts"]/span[@class="certification"]/text()'
            )
            .get()
            .strip()
        )
        release = (
            response.xpath(
                '//div[@class="title ott_false"]/div[@class="facts"]/span[@class="release"]/text()'
            )
            .get()
            .strip()
        )
        genres = response.xpath(
            '//div[@class="title ott_false"]/div[@class="facts"]/span[@class="genres"]//text()'
        ).getall()
        runtime = (
            response.xpath(
                '//div[@class="title ott_false"]/div[@class="facts"]/span[@class="runtime"]/text()'
            )
            .get()
            .strip()
        )
        user_score = response.xpath('//div[@class="user_score_chart"]/@data-percent').get()
        header_info = response.xpath('//div[@class="header_info"]/h3/text()').get()
        overview = response.xpath(
            '//div[@class="header_info"]/div[@class="overview"]/p/text()'
        ).get()
        top_billed_cast = response.xpath(
            '//div[@id="cast_scroller"]/ol[@class="people scroller"]/li/p/a/text()'
        ).getall()
        cast_link = response.xpath(
            '//div[@id="cast_scroller"]/ol[@class="people scroller"]/li[@class="filler view_more"]/p/a/@href'
        ).get()
        budget = response.xpath('//p[strong[bdi[text()="Budget"]]]/text()').get()
        revenue = response.xpath('//p[strong[bdi[text()="Revenue"]]]/text()').get()
        keywords = response.xpath(
            '//section[@class="keywords right_column"]//a[@class="rounded"]/text()'
        ).getall()
        cast_info = response.follow(cast_link, callback=self.parse_cast)
        yield {
            "url": url,
            "title": title,
            "publish_year": publish_year,
            "certification": certification,
            "release": release,
            "genres": genres,
            "runtime": runtime,
            "user_score": user_score,
            "header_info": header_info,
            "overview": overview,
            "top_billed_cast": top_billed_cast,
            "cast_info": cast_info,
            "budget": budget,
            "revenue": revenue,
            "keywords": keywords,
        }

    def parse_cast(self, response):
        cast = response.xpath(
            '//section[@class="panel pad" and h3[contains(text(),"Cast")]]//div[@class="info"]//a/text() | //section[@class="panel pad" and h3[contains(text(),"Cast")]]//div[@class="info"]//p[@class="character"]/text()'
        ).getall()
        crew = response.xpath(
            '//div[@class="crew_wrapper"]//div[@class="info"]//span//a/text() | //div[@class="crew_wrapper"]//div[@class="info"]//span/p[@class="episode_count_crew"]/text()'
        ).getall()
        yield {"cast": cast, "crew": crew}
