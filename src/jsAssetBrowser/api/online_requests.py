from urllib.request import Request, urlopen


def request(url):
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    return urlopen(req).read()
