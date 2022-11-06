# -*- coding: UTF-8 -*-
'''
ocr request using baidu api
'''
import sys

import requests
import base64
import json


def get_access_token(AK, SK):
    # client_id 为官网获取的AK， client_secret 为官网获取的SK
    host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=' + AK + '&client_secret=' + SK
    response = requests.get(host)
    if response:
        print(response.json())
        return response.json()
    else:
        raise 'connot get access token'


class Ocr(object):
    def __init__(self, ocr_config: str):
        self.request_url = "https://aip.baidubce.com/rest/2.0/ocr/v1/accurate_basic"  # 通用高精度
        with open(ocr_config, 'r') as f:
            self.config = json.load(f)
        self.access_token = get_access_token(self.config['API_Key'], self.config['Secret_Key'])['access_token']
        self.request_url = self.request_url + "?access_token=" + self.access_token
        self.headers = {'content-type': 'application/x-www-form-urlencoded'}

    def get(self, f):
        f = open(f, 'rb')
        img = base64.b64encode(f.read())
        params = {"image": img}
        response = requests.post(self.request_url, data=params, headers=self.headers)
        if response:
            print(response.json())
            return response.json()['words_result']
        else:
            print('ocr request failed')

# test ocr
if __name__ == '__main__':
    ocr = Ocr('../data/ocr_config.json')
    ocr.get(r"C:\Users\jia\Desktop\1.jpeg")
