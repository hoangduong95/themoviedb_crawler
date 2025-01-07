# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


import logging

# useful for handling different item types with a single interface
# from itemadapter import ItemAdapter
import re

logger = logging.getLogger(__name__)


class TmdbMoviePipeline:
    def process_item(self, item, spider):
        id = item["url"].split("/")[-1].split("-")[0]
        # publish_year = item["publish_year"].strip("()")
        origin_certification = item["certification"]
        certification = ""
        if origin_certification:
            certification = origin_certification.strip()
        # release = item["release"].strip()
        origin_genres = item["genres"]
        genres = [genre.strip() for genre in origin_genres if re.search(r"\w+", genre)]
        # origin_run_time = item["runtime"]
        # run_time = "NA"
        # if origin_run_time:
        #     run_time = origin_run_time.strip()
        top_billed_cast = item["top_billed_cast"]
        if top_billed_cast:
            top_billed_cast.pop()

        origin_cast = item["cast"]
        actor = []
        if origin_cast:
            actor = list(origin_cast.keys())
        origin_crew = item["crew"]
        director = []
        if origin_crew:
            director = [name for name, roles in origin_crew.items() if "Director" in roles]

        # item["publish_year"] = publish_year
        # item["certification"] = certification
        # item["release"] = release
        # item["genres"] = genres
        # item["runtime"] = run_time
        # item["top_billed_cast"] = top_billed_cast
        # item["actor"] = actor
        # item["director"] = director

        result_item = {
            "url": item["url"],
            "id": id,
            "title": item["title"],
            # "publish_year": publish_year,
            "certification": certification,
            "genres": genres,
            # "run_time": run_time,
            "actor": actor,
            "director": director,
            "keywords": item["keywords"],
        }

        return result_item


class TmdbTvshowPipeline:
    def process_item(self, item, spider):
        # logger.info(f"Processing {item['title']}")
        # publish_year = item["publish_year"].strip("()")
        origin_certification = item["certification"]
        certification = ""
        if origin_certification:
            certification = origin_certification.strip()
        origin_genres = item["genres"]
        genres = [genre.strip() for genre in origin_genres if re.search(r"\w+", genre)]
        top_billed_cast = item["top_billed_cast"]
        if top_billed_cast:
            top_billed_cast.pop()

        origin_cast = item["cast"]
        actor = []
        if origin_cast:
            actor = list(origin_cast.keys())
        origin_crew = item["crew"]
        director = []
        if origin_crew:
            director = [name for name, roles in origin_crew.items() if "Director" in roles]
        # item["publish_year"] = publish_year
        # item["certification"] = certification
        # item["genres"] = genres
        # item["top_billed_cast"] = top_billed_cast
        # item["actor"] = actor
        # item["director"] = director

        result_item = {
            # "publish_year": publish_year,
            "certification": certification,
            "genres": genres,
            # "run_time": run_time,
            "actor": actor,
            "director": director,
        }

        return result_item
