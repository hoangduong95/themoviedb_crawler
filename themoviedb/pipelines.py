# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


import logging

# useful for handling different item types with a single interface
# from itemadapter import ItemAdapter
import re

logger = logging.getLogger(__name__)


class ThemoviedbPipeline:
    def process_item(self, item, spider):
        publish_year = item["publish_year"].strip("()")
        origin_certification = item["certification"]
        certification = ""
        if origin_certification:
            certification = origin_certification.strip()
        release = item["release"].strip()
        origin_genres = item["genres"]
        # # print(publish_year)
        genres = [genre.strip() for genre in origin_genres if re.search(r"\w+", genre)]
        # logger.info(origin_genres)
        # logger.info(genres)
        run_time = item["runtime"].strip()
        origin_cast = item["cast"]
        cast = [member.strip() for member in origin_cast]
        # logger.info(origin_cast)
        # logger.info(cast)
        origin_crew = item["crew"]
        crew = [member.strip() for member in origin_crew]

        item["publish_year"] = publish_year
        item["certification"] = certification
        item["release"] = release
        item["genres"] = genres
        item["runtime"] = run_time
        item["cast"] = cast
        item["crew"] = crew

        return item
