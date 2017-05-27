import urllib.request
from bs4 import BeautifulSoup


def get_soup(url):
    req = urllib.request.Request(url)
    response = urllib.request.urlopen(req)
    html = response.read()
    return BeautifulSoup(html, "lxml")

def format_price(price):
    res = ""
    for n in price:
        res += n.replace(",", "").replace(" ", "").replace("円", "")
    return int(res)

def format_point(point):
    point = point.replace(",", "").replace(" ", "").replace("ポイント", "")
    return format_price(point)

def get_yahoo_lowest(jan):
    url = 'http://shopping.yahoo.co.jp/product/j/{}/compare.html'.format(jan)
    soup = get_soup(url)

    lowest_price = soup.find("div", class_="mdLowestPrice")

    name = lowest_price.find("li", class_="elItemName").text

    a_tag = lowest_price.find("p", class_="elImage").a
    url = a_tag.attrs["href"]
    image = a_tag.img.attrs["src"]

    price = format_price(lowest_price.find("li", class_="elItemPrice").em.text)
    point = format_point(lowest_price.find("li", class_="elItemPoint").text)

    message = lowest_price.find("li", class_="elItemShipping").em.text

    return dict(name=name, url=url, image=image, price=price, point=point, message=message)