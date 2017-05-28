# coding: utf-8

from flask import Flask, request, render_template, flash

from controller import (
    get_jan,
    get_yahoo_lowest,
    get_rakuten_lowest_page,
    get_rakuten_lowest,
    judge_platform,
)


app = Flask(__name__)


@app.route("/")
def index():
    return render_template('top.html')


@app.route('/get_jan_code', methods=['POST'])
def get_jan_code():
    keyword = request.form['keyword']
    jan = get_jan(keyword)
    flash(keyword)
    return render_template('get_jan_code.html', jan=jan)


@app.route('/search', methods=['POST'])
def search():
    select_jan = request.form['select_jan']
    try:
        yahoo = get_yahoo_lowest(select_jan)
    except:
        yahoo = "Yahoo!ショッピングで取り扱っていない可能性のある商品です。"
    try:
        rakuten = get_rakuten_lowest(get_rakuten_lowest_page(select_jan))
    except:
        rakuten = "楽天市場で取り扱っていない可能性のある商品です。"

    if type(yahoo) == str or type(rakuten) == str:
        judges = [yahoo, rakuten]
    else:
        judges = []
        point_result = judge_platform(yahoo, rakuten, True)
        if point_result[0] == "yahoo":
            judges += [yahoo, rakuten, point_result[1]]
        else:
            judges += [rakuten, yahoo, point_result[1]]

        result = judge_platform(yahoo, rakuten, False)
        if result[0] == "yahoo":
            judges += [yahoo, rakuten, result[1]]
        else:
            judges += [rakuten, yahoo, result[1]]

    return render_template('product.html', judges=judges)


if __name__ == "__main__":
    app.run()
