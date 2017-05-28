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
    item_list = []
    for i in range(2):
        url = 'http://askillers.com/jan/?index={0}&word={1}/'.format(i+1, urllib.parse.quote(keyword))
        soup = get_soup(url)

        items = soup.find_all("div", class_="item")

        for item in items:
            try:
                item_texts = item.find_all("div")[-1].text
                name = item_texts.split("\n\t")[1]
                jan = item_texts.split("\n\t")[2].replace("JAN/EAN:", "")

                try:
                    image = item.img.attrs["src"].replace("SL75", "SL200")
                except:
                    image = ""

                if not image:
                    image = "https://5svbqa.dm2302.livefilestore.com/y4mpKgYWEBbDosjMNCVgY4wilQDn8k0EICNdM7YDUkqpgF8h062iXiGqiQfzJNWbdhACEHDHZH-UUoJVU5E-Kwe4mCIrpFYGPMw1yNTfzitAF59P7a3JnZZqOB2K8d6FI8WQ4KbXy-56nqsImYc3BVmtxw702o44B_2g7r2C_yIc60S7xRxbROelwuS9ybC500k0Pi8jeVgUlhq3pNI_j9EuQ?width=200&height=200&cropmode=none"

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

    return dict(name=name, url=url, image=image, price=price, point=point, message=message, platform="Yahoo!ショッピング")


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

    image = soup.find("div", class_="itemThumb").img.attrs["src"]
    a_tag = lowest_item.find("div", class_="quickViewIteminfo").a
    name = a_tag.text
    url = a_tag.attrs["href"]

    price = format_number(lowest_item.find("span", class_="itemPrice3").text, "円")
    point = format_number(lowest_item.find("span", class_="pointGet").text, "ポイント")

    try:
        message = lowest_item.find("span", class_="shipfree").text
    except:
        message = ""

    return dict(name=name, url=url, image=image, price=price, point=point, message=message, platform="楽天市場")
