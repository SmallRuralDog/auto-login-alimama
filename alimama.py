# coding:utf-8
import datetime
import json
import time

import requests
from selenium import webdriver


class Spider(object):
    def __init__(self):
        self.web = webdriver.Chrome()
        self.headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-CN,zh;q=0.8,en;q=0.6',
            'cache-control': 'max-age=0',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.78 Safari/537.36'
        }
        self.req = requests.Session()
        self.cookies = {}

    def login(self):
        self.web.get(
            'https://login.taobao.com/member/login.jhtml?style=mini&newMini2=true&css_style=alimama&from=alimama&redirectURL=http%3A%2F%2Fwww.alimama.com&full_redirect=true&disableQuickLogin=true')

        i = input('请确认是否已登录？[y/n]:')
        if (i != 'y'):
            return

        self.web.get('http://pub.alimama.com/myunion.htm')
        cookie = ''
        for elem in self.web.get_cookies():
            cookie += elem["name"] + "=" + elem["value"] + ";"
            if elem["name"] == '_tb_token_':
                self.token = elem["value"]
        self.cookies = cookie
        self.headers['Cookie'] = self.cookies
        self.web.quit()

    # 获取淘宝客订单列表
    def get_taoke_order_list(self):
        s_day = datetime.date.today() - datetime.timedelta(days=90)
        e_day = datetime.date.today() - datetime.timedelta(days=1)
        url = 'https://pub.alimama.com/report/getTbkPaymentDetails.json?startTime=' + s_day.strftime(
            "%Y-%m-%d") + '&endTime=' + e_day.strftime(
            "%Y-%m-%d") + '&payStatus=&queryType=1&toPage=1&perPageSize=20'
        print(url)
        web_data = self.req.get(url, headers=self.headers)
        data = json.loads(web_data.text)
        print(data)


if __name__ == '__main__':
    sp = Spider()
    sp.login()
    while True:
        sp.get_taoke_order_list()
        time.sleep(30)
