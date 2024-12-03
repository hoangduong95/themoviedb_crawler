import scrapy


class TmdbTvshowsSpider(scrapy.Spider):
    name = "TMDB_TVShows"
    allowed_domains = ["www.themoviedb.org"]
    start_urls = ["https://www.themoviedb.org/tv"]

    def parse(self, response):
        pass
