# coding: utf-8

import urllib.request
from bs4 import BeautifulSoup


def get_soup(url):
    req = urllib.request.Request(url)
    response = urllib.request.urlopen(req)
    html = response.read()
    return BeautifulSoup(html, "lxml")

def format_number(number, sign):
    res = ""
    for n in number.replace(sign, ""):
        res += n.replace(",", "").replace(" ", "")
    return int(res)


def get_jan(keyword):
    url = 'http://askillers.com/jan/?index=1&word={}/'.format(urllib.parse.quote(keyword))
    soup = get_soup(url)

    items = soup.find_all("div", class_="item")

    item_list = []
    for item in items:
        try:
            item_texts = item.find_all("div")[-1].text
            name = item_texts.split("\n\t")[1]
            jan = item_texts.split("\n\t")[2].replace("JAN/EAN:", "")

            try:
                image = item.img.attrs["src"]
            except:
                image = ""

            item_list += [dict(name=name, jan=jan, image=image)]
        except:
            pass

    return item_list


def get_yahoo_lowest(jan):
    url = 'http://shopping.yahoo.co.jp/product/j/{}/compare.html'.format(jan)
    soup = get_soup(url)

    lowest_price = soup.find("div", class_="mdLowestPrice")

    name = lowest_price.find("li", class_="elItemName").text

    a_tag = lowest_price.find("p", class_="elImage").a
    url = a_tag.attrs["href"]
    image = a_tag.img.attrs["src"]

    price = format_number(lowest_price.find("li", class_="elItemPrice").em.text, "円")
    point = format_number(lowest_price.find("li", class_="elItemPoint").text, "ポイント")

    try:
        message = lowest_price.find("li", class_="elItemShipping").em.text
    except:
        message = ""

    return dict(name=name, url=url, image=image, price=price, point=point, message=message)


def get_rakuten_lowest_page(jan):
    url = 'http://search.rakuten.co.jp/search/mall/{}/'.format(jan)
    soup = get_soup(url)

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


def get_rakuten_lowest(url):
    soup = get_soup(url)

    lowest_item = soup.find("tr", class_="specColumnUsed")

    a_tag = lowest_item.find("div", class_="quickViewIteminfo").a
    name = a_tag.text
    url = a_tag.attrs["href"]

    price = format_number(lowest_item.find("span", class_="itemPrice3").text, "円")
    point = format_number(lowest_item.find("span", class_="pointGet").text, "ポイント")

    try:
        message = lowest_item.find("span", class_="shipfree").text
    except:
        message = ""

    return dict(name=name, url=url, price=price, point=point, message=message)
