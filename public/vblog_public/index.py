# -*- coding:utf-8 -*-
# 作者：IT小学生蔡坨坨
# 时间：2021/1/9 21:20


class VBlog:
    def __init__(self, requests):
        self.requests = requests

    def get_cookie(self):
        """获取cookie"""
        url_v_login = "http://182.92.178.83:8081/login"
        # 定义参数，字典格式
        payload = {'username': 'sang', 'password': '123'}
        result = self.requests.post(url_v_login, data=payload)
        # 获取RequestsCookieJar
        result_cookie = result.cookies
        # 将RequestsCookieJar转化为字典格式
        result_cookie_dic = self.requests.utils.dict_from_cookiejar(result_cookie)
        # 获取SESSION
        final_cookie = "JSESSIONID=" + result_cookie_dic["JSESSIONID"]  # SJSESSIONID=D042C5FE4CFF337806D545B0001E7197
        return final_cookie
