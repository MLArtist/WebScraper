from collections import Counter
from bs4 import BeautifulSoup
from webscraper.utils.url_utils import url_split


def get_links(text, website_full_url):
    """
    get the local links and their frequency in a webpage
    :param
        text: response.text
        website_full_url: homepage of website which is being scrapped
    """

    local_urls = list()
    foreign_urls = list()

    base = url_split(website_full_url)["base"]
    strip_base = url_split(website_full_url)["strip_base"]
    base_url = url_split(website_full_url)["base_url"]
    path = url_split(website_full_url)["path"]
    scheme = url_split(website_full_url)["scheme"]

    soup = BeautifulSoup(text, "lxml")

    for link in soup.find_all("a"):
        anchor = link.attrs.get("href").strip() if "href" in link.attrs else ''
        if anchor.startswith('//'):
            endchar = anchor[-1] if anchor.endswith("/") else ""
            anchor = anchor.strip("/") + endchar
        if anchor.startswith('javascript'): continue
        if ("#" in anchor or anchor.startswith("mailto:")
                or anchor.startswith("tel:")):
            continue
        elif anchor.startswith('/'):
            local_link = base_url + anchor
            local_urls.append(local_link)
        elif anchor.startswith("http") and strip_base.lower() in anchor[
                        :anchor.find("/", anchor.find("//") + 2)].lower():
            local_urls.append(anchor)
        elif strip_base.lower() in anchor[:anchor.find("/")].lower():
            local_link = "{}://{}".format(scheme, anchor)
            local_urls.append(local_link)
        elif not anchor.lower().startswith("http"):
            local_link = path + anchor
            local_urls.append(local_link)
        else:
            foreign_urls.append(anchor)
    return dict(Counter(local_urls))


if __name__ == '__main__':
    # get_links(text, website_full_url)
    pass
