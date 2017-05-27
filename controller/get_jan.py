import urllib.request
from bs4 import BeautifulSoup


def get_jan(keyword):
    url = 'http://askillers.com/jan/?index=1&word={}/'.format(urllib.parse.quote(keyword))
    req = urllib.request.Request(url)
    response = urllib.request.urlopen(req)
    html = response.read()
    soup = BeautifulSoup(html, "lxml")

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
