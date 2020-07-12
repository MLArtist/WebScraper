import argparse
import json
import os
import sys
import time
import uuid
from random import randint
from utils.extract_links_from_webpage import get_links
from utils.request_client import ReqestClient
from utils.url_utils import get_filtered_links
import config
from utils.redislite_utils import redis_cleanup, redis_client as redis

request_client = ReqestClient()


def write_url_data(url, response_text):
    if not os.path.exists(config.DATA_DIR):
        os.mkdir(config.DATA_DIR)
    file_path = config.DATA_DIR + str(uuid.uuid3(uuid.NAMESPACE_URL, str(url))) + ".json"
    if not os.path.exists(file_path):
        with open(file_path, "w") as fp:
            json.dump({url: response_text}, fp)


class Websitescrap:
    def __init__(self, url, start_afresh=False):
        self.url = url
        if start_afresh:
            redis.flushdb()
            redis.sadd("new_urls", url)

    def crawl(self, sleep_time_lower=30, sleep_time_upper=121):
        print("\ncrawling started\n")
        write_count = 0
        write_flag = 1
        while len(redis.smembers("new_urls")):
            url = redis.spop("new_urls")
            redis.sadd("processed_urls", url)

            if write_count % 12 == 0:
                time.sleep(randint(sleep_time_lower, sleep_time_upper))
            else:
                time.sleep(randint(sleep_time_lower, int(sleep_time_upper / 2)))

            if write_count % write_flag == 0:
                print('Processing %s' % url)

            write_count += 1
            # if write_count > 13:
            #     break

            response = request_client.request_with_proxy_header(url)
            if not response or not response.status_code == 200:
                continue

            # write response.text to a json dump file
            write_url_data(url, response.text)

            # get the urls for local page
            local_urls = [*get_links(response.text, self.url).keys()]

            # filter the urls of foreign urls or dummy urls
            local_urls = get_filtered_links(local_urls, self.url)

            for i in local_urls:
                if not redis.sismember("processed_urls", i):
                    redis.sadd("new_urls", i)
            redis_cleanup(self.url)
            if write_count % write_flag == 0:
                print('Processed')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('website_address')
    parser.add_argument("-s", "--start_afresh", help="whether to start a fresh crawling", default=True, action='store',
                        dest='start_afresh')

    args = parser.parse_args()
    website = args.website_address
    start_afresh = args.start_afresh

    if not website.startswith("http"):
        print("\033[91m {}\033[00m".format("Please include website scheme (http/https) in the provided address"))
        return

    scrapper = Websitescrap(website, start_afresh=start_afresh)
    scrapper.crawl(5, 18)


if __name__ == '__main__':
    main()
