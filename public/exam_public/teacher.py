# -*- coding:utf-8 -*-
# 作者：IT小学生蔡坨坨
# 时间：2021/1/9 23:06


class Teacher:
    def __init__(self, requests):
        self.requests = requests

    def get_cookie(self):
        """自动获取cookie"""
        # 调用登录接口
        url_login = "http://182.92.178.83:8088/api/user/login"
        # 传入用户名和密码
        payload = {"userName": "admin", "password": "123456", "remember": False}
        # 返回结果赋值给result
        result = self.requests.post(url_login, json=payload)
        # 获取RequestsCookieJar
        result_cookie = result.cookies
        # 将RequestsCookieJar转化为字典格式
        result_cookie_dic = self.requests.utils.dict_from_cookiejar(result_cookie)
        # 获取SESSION
        final_cookie = "SESSION=" + result_cookie_dic["SESSION"]  # SESSION=Mzc2...
        return final_cookie

    def delete_paper(self, paper_id):
        """删除试卷"""
        headers = {"Cookie": Teacher(self.requests).get_cookie()}
        url_delete = "http://182.92.178.83:8088/api/admin/exam/paper/delete/" + paper_id
        result = self.requests.post(url_delete, headers=headers)
        return result
