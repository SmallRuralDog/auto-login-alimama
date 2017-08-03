# coding:utf-8
import json
import time

import requests
from selenium import webdriver


class Spider(object):
    def __init__(self):
        self.web = webdriver.Chrome()
        self.__username = '淘宝账号'
        self.__password = '淘宝密码'
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
    #登录
    def login(self):
        self.web.get(
            'https://login.taobao.com/member/login.jhtml?style=mini&newMini2=true&css_style=alimama&from=alimama&redirectURL=http%3A%2F%2Fwww.alimama.com&full_redirect=true&disableQuickLogin=true')
        self.web.find_element_by_class_name('login-switch').click()

        self.web.find_element_by_id('TPL_username_1').send_keys(self.__username)
        self.web.find_element_by_id('TPL_password_1').send_keys(self.__password)
        time.sleep(2)
        self.web.find_element_by_id('J_SubmitStatic').click()
        # 等待5秒
        time.sleep(5)
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
        url = 'http://pub.alimama.com/report/getTbkPaymentDetails.json?startTime=2017-05-28&endTime=2017-08-03&payStatus=&queryType=1&toPage=1&perPageSize=50&total=&t=1501747895837&pvid=&_tb_token_=7fG7CEIuRsq&_input_charset=utf-8'
        web_data = self.req.get(url, headers=self.headers)

        data = json.loads(web_data.text)
        print(data['data']['paymentList'])

    #创建推广位
    def add_ad(self):
        name = input()
        res = self.req.post('http://pub.alimama.com/common/adzone/selfAdzoneCreate.json', data={
            'tag': '29',
            'gcid': '8',
            'siteid': '24082855',
            'selectact': 'add',
            'newadzonename': name,
            '_tb_token_': self.token
        }, headers=self.headers)

        print(res.text)
    #获取推广位列表
    def get_ad_list(self):
        res = self.req.get(
            'http://pub.alimama.com/common/adzone/adzoneManage.json?tab=3&toPage=1&perPageSize=40&gcid=8',
            headers=self.headers)
        print(res.text)


if __name__ == '__main__':
    sp = Spider()
    sp.login()
    sp.add_ad()
    sp.get_ad_list()
    for i in range(1000):
        sp.get_taoke_order_list()
        time.sleep(30)
