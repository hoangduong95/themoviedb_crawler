import logging

import scrapy

logger = logging.getLogger(__name__)


class TmdbMoviesSpider(scrapy.Spider):
    name = "TMDB_Movies"
    allowed_domains = ["www.themoviedb.org"]
    start_urls = ["https://www.themoviedb.org/movie"]
    custom_settings = {
        "ITEM_PIPELINES": {
            "themoviedb.pipelines.TmdbMoviePipeline": 300,
        }
    }
    pagination_count = 0

    def parse(self, response):
        logger.info(response.url)
        self.pagination_count += 1
        movie_items = response.xpath(
            '//div[@class="media_items results"]//div[@class="content"]//a/@href'
        )
        yield from response.follow_all(movie_items, callback=self.parse_movie)
        next_page = response.xpath('//p[@class="load_more"]/a[text()="Load More"]/@href').get()
        if (
            next_page is not None
            and self.pagination_count <= 0  # bỏ điều kiện về pagination_count nếu chạy thật
        ):
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)

    def parse_movie(self, response):
        url = response.url
        title = response.xpath('//div[@class="title ott_false"]/h2/a/text()').get()
        publish_year = response.xpath('//div[@class="title ott_false"]/h2//span/text()').get()
        certification = response.xpath(
            '//div[@class="title ott_false"]/div[@class="facts"]/span[@class="certification"]/text()'
        ).get()
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
            '//section[@class="keywords right_column"]//a[@class="rounded" or @class="!border !border-tmdb-light-blue font-semibold"]/text()'
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
        cast_link = response.xpath(
            '//p[@class="new_button"]/a[text()="Full Cast & Crew"]/@href'
        ).get()
        if cast_link:
            yield response.follow(
                cast_link, callback=self.parse_cast, cb_kwargs={"movie_item": movie_item}
            )
        else:
            movie_item["cast"] = None
            movie_item["crew"] = None
            yield movie_item

    def parse_cast(self, response, movie_item):
        cast_elements = response.xpath(
            '//section[@class="panel pad" and h3[contains(text(),"Cast")]]//div[@class="info"]'
        )
        cast = {}
        for cast_element in cast_elements:
            actor = cast_element.xpath("p[1]/a/text()").get()
            character = cast_element.xpath('p[@class="character"]/text()').get()
            cast[actor] = character.strip()
        movie_item["cast"] = cast

        crew_elements = response.xpath('//div[@class="crew_wrapper"]//div[@class="info"]/span')
        crew = {}
        for crew_element in crew_elements:
            crew_member = crew_element.xpath("p[1]/a/text()").get()
            role_raw = crew_element.xpath('p[@class="episode_count_crew"]/text()').get()

            role = []
            if role_raw:
                role = [element.strip() for element in role_raw.split(",")]
            if crew_member in crew:
                crew[crew_member].extend(role)
            else:
                crew[crew_member] = role
        movie_item["crew"] = crew
        yield movie_item
