import urllib.request
from bs4 import BeautifulSoup


def get_rakuten_lowest_page(jan):
    url = 'http://search.rakuten.co.jp/search/mall/{}/'.format(jan)
    req = urllib.request.Request(url)
    response = urllib.request.urlopen(req)
    html = response.read()
    soup = BeautifulSoup(html, "lxml")

    items = soup.find_all("div", class_="rsrSResultSect")

    for item in items:
        item_info = item.find("div", class_="rsrSResultItemInfo")
        url = ""

        try:
            url = item_info.find("p", class_="product").a.attrs["href"]
            break
        except:
            pass

    return url
