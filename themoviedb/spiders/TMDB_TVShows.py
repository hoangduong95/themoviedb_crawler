import logging

import scrapy

logger = logging.getLogger(__name__)


class TmdbTvshowsSpider(scrapy.Spider):
    name = "TMDB_TVShows"
    allowed_domains = ["www.themoviedb.org"]
    start_urls = ["https://www.themoviedb.org/tv"]
    custom_settings = {
        "ITEM_PIPELINES": {
            "themoviedb.pipelines.TmdbTvshowPipeline": 300,
        }
    }

    pagination_count = 0

    def parse(self, response):
        logger.info(response.url)
        self.pagination_count += 1
        tvshow_items = response.xpath(
            '//div[@class="media_items results"]//div[@class="content"]//a/@href'
        )
        yield from response.follow_all(tvshow_items, callback=self.parse_tvshow)
        next_page = response.xpath('//p[@class="load_more"]/a[text()="Load More"]/@href').get()
        if (
            next_page is not None
            and self.pagination_count <= 5  # bỏ điều kiện về pagination_count nếu chạy thật
        ):
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)

    def parse_tvshow(self, response):
        url = response.url
        logger.info(url)
        title = response.xpath('//div[contains(@class,"title")]/h2/a/text()').get()
        publish_year = response.xpath('//div[contains(@class,"title")]/h2//span/text()').get()
        certification = response.xpath(
            '//div[contains(@class,"title")]/div[@class="facts"]/span[@class="certification"]/text()'
        ).get()
        genres = response.xpath(
            '//div[contains(@class,"title")]/div[@class="facts"]/span[@class="genres"]//text()'
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
        last_season = response.xpath(
            '//div[@class="season card"]//div[@class="content"]//h2/a/text()'
        ).get()
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
            "last_season": last_season,
        }
        cast_link = response.xpath(
            '//p[@class="new_button"]/a[text()="Full Cast & Crew"]/@href'
        ).get()
        seasons_desc_link = response.xpath(
            '//p[@class="new_button"]/a[text()="View All Seasons"]/@href'
        ).get()
        if cast_link:
            yield response.follow(
                cast_link,
                callback=self.parse_cast,
                cb_kwargs={"tvshow_item": tvshow_item, "seasons_desc_link": seasons_desc_link},
            )
        elif seasons_desc_link:
            tvshow_item["cast"] = None
            tvshow_item["crew"] = None
            yield response.follow(
                cast_link, callback=self.parse_seasons, cb_kwargs={"tvshow_item": tvshow_item}
            )
        else:
            tvshow_item["cast"] = None
            tvshow_item["crew"] = None
            tvshow_item["seasons"] = None
            yield tvshow_item

    def parse_cast(self, response, tvshow_item, seasons_desc_link):
        cast_elements = response.xpath(
            '//section[@class="panel pad" and h3[contains(text(),"Cast")]]//div[@class="info"]/span'
        )
        cast = {}
        for cast_element in cast_elements:
            actor = cast_element.xpath("p[1]/a/text()").get()
            character = cast_element.xpath('p[@class="character"]/a/text()').getall()
            cast[actor] = ",".join(character)
        tvshow_item["cast"] = cast

        crew_elements = response.xpath('//div[@class="crew_wrapper"]//div[@class="info"]/span')
        crew = {}
        for crew_element in crew_elements:
            crew_member = crew_element.xpath("p[1]/a/text()").get()
            role = crew_element.xpath('p[@class="episode_count_crew"]/a/text()').getall()
            crew[crew_member] = [role_element.strip() for role_element in role]
        tvshow_item["crew"] = crew

        if seasons_desc_link:
            yield response.follow(
                seasons_desc_link,
                callback=self.parse_seasons,
                cb_kwargs={"tvshow_item": tvshow_item},
            )
        else:
            yield tvshow_item

    def parse_seasons(self, response, tvshow_item):
        # logger.info(response.url)
        seasons = response.xpath('//div[@class="season"]//div[@class="content"]')
        seasons_dict = {}
        for season in seasons:
            key = season.xpath(".//div//a/text()").get()
            season_release = ("").join(season.xpath(".//h4/text()").getall()).strip()
            season_premier = season.xpath('.//div[@class="season_overview"]/p[1]/text()').get()
            season_desc = "Not available"
            season_desc_tmdb = season.xpath('.//div[@class="season_overview"]/p[2]/text()').get()
            if season_desc_tmdb:
                season_desc = season_desc_tmdb
            seasons_dict[key] = {
                "season_release": season_release,
                "season_premier": season_premier,
                "season_desc": season_desc,
            }
        tvshow_item["seasons_dict"] = seasons_dict
        yield tvshow_item
