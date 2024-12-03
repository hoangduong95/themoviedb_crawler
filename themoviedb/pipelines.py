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
        publish_year = item["publish_year"].strip("()")
        origin_certification = item["certification"]
        certification = ""
        if origin_certification:
            certification = origin_certification.strip()
        release = item["release"].strip()
        origin_genres = item["genres"]
        genres = [genre.strip() for genre in origin_genres if re.search(r"\w+", genre)]
        origin_run_time = item["runtime"]
        run_time = "NA"
        if origin_run_time:
            run_time = origin_run_time.strip()
        top_billed_cast = item["top_billed_cast"]
        if top_billed_cast:
            top_billed_cast.pop()

        origin_cast = item["cast"]
        actor = []
        if origin_cast:
            cast = [member.strip() for member in origin_cast]
            character_to_actor = map_crew(cast)
            actor = [name for names in character_to_actor.values() for name in names]
        else:
            cast = []
        origin_crew = item["crew"]
        director = []
        if origin_crew:
            crew = [member.strip() for member in origin_crew]
            role_to_crew = map_crew(crew)
            director = role_to_crew.get("Director", [])
        else:
            crew = []

        item["publish_year"] = publish_year
        item["certification"] = certification
        item["release"] = release
        item["genres"] = genres
        item["runtime"] = run_time
        item["top_billed_cast"] = top_billed_cast
        item["cast"] = cast
        item["actor"] = actor
        item["crew"] = crew
        item["director"] = director

        return item


def map_crew(array):
    role_map = {}
    for i in range(0, len(array), 2):
        person = array[i]
        role = array[i + 1]
        if role not in role_map:
            role_map[role] = []
        role_map[role].append(person)

    return role_map
