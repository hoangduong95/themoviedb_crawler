import asyncio
import logging

import scrapy

logger = logging.getLogger(__name__)


class ThemoviedbSpider(scrapy.Spider):
    name = "TheMovieDB"
    allowed_domains = ["www.themoviedb.org"]
    start_urls = ["https://www.themoviedb.org/movie?page=2"]

    retry_url_pattern = r"https:\/\/www\.themoviedb\.org\/movie\/\d+(-[a-zA-Z0-9\-]+)*"
    title_element = '//div[@class="title ott_false"]/h2/a/text()'
    certification_element = (
        '//div[@class="title ott_false"]/div[@class="facts"]/span[@class="certification"]/text()'
    )

    def parse(self, response):
        # logger.info(response.request.headers['User-Agent'])
        items = response.xpath(
            '//div[@class="media_items results"]//div[@class="content"]//a/@href'
        )
        yield from response.follow_all(items, callback=self.parse_item)

    async def parse_item(self, response):

        url = response.url
        title = response.xpath(self.title_element).get()
        publish_year = response.xpath('//div[@class="title ott_false"]/h2//span/text()').get()
        certification = response.xpath(self.certification_element).get()
        release = response.xpath(
            '//div[@class="title ott_false"]/div[@class="facts"]/span[@class="release"]/text()'
        ).get()
        genres = response.xpath(
            '//div[@class="title ott_false"]/div[@class="facts"]/span[@class="genres"]//text()'
        ).getall()
        runtime = response.xpath(
            '//div[@class="title ott_false"]/div[@class="facts"]/span[@class="runtime"]/text()'
        ).get()
        user_score = response.xpath('//div[@class="user_score_chart"]/@data-percent').get()
        header_info = response.xpath('//div[@class="header_info"]/h3/text()').get()
        overview = response.xpath(
            '//div[@class="header_info"]/div[@class="overview"]/p/text()'
        ).get()
        top_billed_cast = response.xpath(
            '//div[@id="cast_scroller"]/ol[@class="people scroller"]/li/p/a/text()'
        ).getall()
        budget = response.xpath('//p[strong[bdi[text()="Budget"]]]/text()').get()
        revenue = response.xpath('//p[strong[bdi[text()="Revenue"]]]/text()').get()
        keywords = response.xpath(
            '//section[@class="keywords right_column"]//a[@class="rounded"]/text()'
        ).getall()
        movie_item = {
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
            "budget": budget,
            "revenue": revenue,
            "keywords": keywords,
        }
        # cast_link = response.xpath(
        #     '//div[@id="cast_scroller"]/ol[@class="people scroller"]/li[@class="filler view_more"]/p/a/@href'
        # ).get()
        cast_link = response.xpath(
            '//p[@class="new_button"]/a[text()="Full Cast & Crew"]/@href'
        ).get()
        # logger.info(cast_link)
        yield response.follow(cast_link, callback=self.parse_cast, meta={"item": movie_item})

    async def parse_cast(self, response):
        # await asyncio.sleep(2)
        movie_item = response.meta["item"]
        movie_item["cast"] = response.xpath(
            '//section[@class="panel pad" and h3[contains(text(),"Cast")]]//div[@class="info"]//a/text() | //section[@class="panel pad" and h3[contains(text(),"Cast")]]//div[@class="info"]//p[@class="character"]/text()'
        ).getall()
        movie_item["crew"] = response.xpath(
            '//div[@class="crew_wrapper"]//div[@class="info"]//span//a/text() | //div[@class="crew_wrapper"]//div[@class="info"]//span/p[@class="episode_count_crew"]/text()'
        ).getall()
        yield movie_item

        # Mot so elements ko kip load khi scrapy lam viec -> scrape gia tri None
