# -*- coding:utf-8 -*-
# 作者：IT小学生蔡坨坨
# 时间：2021/1/9 21:20


class Student:
    def __init__(self, requests):
        self.requests = requests  # 设置全局参数

    def get_cookie(self):
        """获取cookie"""

        # 调用登录接口
        url_login = "http://182.92.178.83:8088/api/user/login"
        # 传入用户名和密码
        payload = {"userName": "ctt01", "password": "123456", "remember": False}
        # 返回结果赋值给result
        result = self.requests.post(url_login, json=payload)
        # 将返回结果转为json格式
        result_json = result.json()
        # print(result_json)
        # 获取RequestsCookieJar
        result_cookie = result.cookies
        # print(result_cookie, type(result_cookie))  # RequestsCookieJar
        # 将RequestsCookieJar转化为字典格式
        result_cookie_dic = self.requests.utils.dict_from_cookiejar(result_cookie)
        # print(result_cookie_dic)  # {'SESSION': 'YzFkM2IzN2QtZWY1OC00Nzc4LTgyOWYtNjg5OGRiZDZlM2E4'}
        # 获取SESSION
        final_cookie = "SESSION=" + result_cookie_dic["SESSION"]  # SESSION=Mzc2...
        return final_cookie
