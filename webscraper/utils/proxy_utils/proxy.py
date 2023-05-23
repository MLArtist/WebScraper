import json
import os
import random
import requests
from bs4 import BeautifulSoup

from webscraper.config import HOME_DIR
from webscraper.utils.user_agent_utils.user_agent import UserAgent

ua = UserAgent()


class Proxy:
    def __init__(self):
        self.proxy_list = self.read_proxy_list()
        if not self.proxy_list:
            self.proxy_list = self.update_proxy_list()
            self.write_proxy_list()
        self.count = 0
        self.proxy = None

    @staticmethod
    def read_proxy_list():
        filename = os.path.join(HOME_DIR, "utils/proxy_utils/proxy_list.json")
        if os.path.exists(filename):
            with open(filename, "r") as fp:
                return json.load(fp)
        return None

    @staticmethod
    def update_proxy_list():
        # Retrieve latest proxies
        url = 'https://www.sslproxies.org/'
        try:
            response = requests.get(url, headers={'User-Agent': ua.user_agent()})
        except:
            raise Exception("Could not scrape proxies from {}!".format(url))

        soup = BeautifulSoup(response.text, 'html.parser')

        proxies_table = soup.find(id='proxylisttable')
        proxy_list = []
        # Save proxies in a file array
        for row in proxies_table.tbody.find_all('tr'):
            proxy_list.append(row.find_all('td')[0].string + ':' + row.find_all('td')[1].string)
        return proxy_list

    def write_proxy_list(self):
        with open("proxy_list.json", "w") as fp:
            json.dump(self.proxy_list, fp)

    def generate_proxy(self):
        """Choose a random proxy; keeps the same proxy for some number of times then changes it
        """
        if self.count % 10 == 0:
            self.proxy = random.choice(self.proxy_list)
        return {
            "http": self.proxy,
            "https": self.proxy
        }


if __name__ == '__main__':
    pro = Proxy()
    print(pro.generate_proxy())
