from requests.auth import HTTPProxyAuth

from utils.proxy_utils.proxy import Proxy, ua
import requests
import config


class ReqestClient(Proxy):
    def __init__(self):
        super().__init__()

    def request_with_proxy_header(self, url):
        header = {'User-Agent': ua.user_agent()}

        if config.USE_PROXY_SERVER:
            proxy = self.generate_proxy()
            auth = HTTPProxyAuth("", "")
            try:
                response = requests.get(url, proxies=proxy, auth=auth, headers=header, timeout=20, verify=True)
                return response
            except:
                # remove the invalid proxy from the proxy list and update in the file
                self.proxy_list.remove(proxy.get("http"))
                self.write_proxy_list()
        else:
            try:
                response = requests.get(url, headers=header, timeout=20, verify=True)
            except:
                response = None

        return response


if __name__ == '__main__':
    cli = ReqestClient()
    print(cli.request_with_proxy_header("https://www.wikipedia.org/").text)
