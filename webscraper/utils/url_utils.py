from urllib.parse import urlsplit

from webscraper.utils.media_extensions import media_extensions_list


def url_split(url):
    """ split the link into useful parts"""
    parts = urlsplit(url)
    scheme = parts.scheme
    base = '{0.netloc}'.format(parts)
    strip_base = base.replace('www.', "")
    base_url = "{0.scheme}://{0.netloc}".format(parts)
    path = url[:url.rfind('/') + 1] if '/' in parts.path else url
    return {
        "scheme": scheme,
        "base": base,
        "strip_base": strip_base,
        "base_url": base_url,
        "path": path
}


def get_filtered_links(local_urls_list, website_full_url):
    """ get the filtered links for a list of local links"""
    filtered_list = []
    strip_base = url_split(website_full_url)["strip_base"].lower()
    for anchor in local_urls_list:
        #discard media extensions
        i = anchor.lower()
        if i[i.rfind("."):].strip("/") in media_extensions_list:
            continue
        # discard anchor tags
        if "#" in i:
            continue
        # discard javascripts tags
        if "javascript:" in i:
            continue
        if i.startswith("http"):
            # discard "https://www.google.com/c.org"
            http_loc = i.find("//")
            end_finder = i.find("/", http_loc+2) if not i.find("/", http_loc+2) == -1 else len(i)
            if not strip_base in i[:end_finder]:
                continue
        else:
            i = i.strip("/")
            # discard "www.google.com/https://www.wikipedia.org"
            end_finder = i.find("/") if not i.find("/") == -1 else len(i)
            if not strip_base in i[:end_finder]:
                continue
        filtered_list.append(anchor)
    return filtered_list


if __name__ == '__main__':
    pass