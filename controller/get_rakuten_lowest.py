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

def get_rakuten_lowest(url):
    soup = get_soup(url)

    lowest_item = soup.find("tr", class_="specColumnUsed")

    a_tag = lowest_item.find("div", class_="quickViewIteminfo").a
    name = a_tag.text
    url = a_tag.attrs["href"]

    price = format_price(lowest_item.find("span", class_="itemPrice3").text)
    point = format_point(lowest_item.find("span", class_="pointGet").text)
    message = lowest_item.find("span", class_="shipfree").text

    return dict(name=name, url=url, price=price, point=point, message=message)
