import unittest
import requests
from public.exam_public.student import Student
import time


class StudentCase(unittest.TestCase):
    def setUp(self):
        self.requests = requests

    def tearDown(self):
        pass

    def test_001_register(self):
        """考试系统前台_学生注册"""
        # 通过用户名拼接时间戳的形式来保证用户名未注册
        now_time = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))  # 20210110122823
        print(now_time)
        payload = {"userName": "ctt" + now_time, "password": "123456", "userLevel": 1}
        result = self.requests.post("http://182.92.178.83:8088/api/student/user/register", json=payload)
        result_json = result.json()
        print(result_json)
        act = result_json["message"]
        exp = "成功"
        # 注册成功，返回结果中message==成功
        self.assertEqual(act, exp)

    def test_002_login(self):
        """考试系统前台_学生登录"""
        url_login = "http://182.92.178.83:8088/api/user/login"
        user_name = "ctt01"
        payload = {"userName": user_name, "password": "123456", "remember": False}
        result = self.requests.post(url_login, json=payload)
        result_json = result.json()
        print(result_json)
        exp = user_name
        try:
            act = result_json["response"]["userName"]
        except KeyError:  # 避免取不到key报错
            act = 666
        print(act)
        # 设置断言，返回结果中包含用户名
        self.assertEqual(exp, act)

    def test_003_user_info(self):
        """考试系统前台_查看个人信息"""
        headers = {"Cookie": Student(self.requests).get_cookie()}
        result = self.requests.post("http://182.92.178.83:8088/api/student/user/current", headers=headers)
        print(result.json())
        act = result.json()["response"]["userName"]
        # 断言结果，返回的用户名是当前账号的用户名
        self.assertEqual(act, "ctt01")

    def test_004_user_info_update(self):
        """考试系统前台_修改个人资料"""
        now_time = time.strftime("%Y%m%d%H%M%S", time.localtime(time.time()))
        real_name = "蔡坨坨" + now_time
        payload = {"id": 25261,
                   "userUuid": "aa1eeb04-f676-4a95-949c-6fe0a4eab85b",
                   "userName": "ctt01",
                   "realName": real_name,
                   "age": 12,
                   "role": 1,
                   "sex": 1,
                   "birthDay": "2020-12-07 00:00:00",
                   "phone": "15059224492",
                   "status": 1, "userLevel": 12,
                   "imagePath": ""}
        headers = {"Cookie": Student(self.requests).get_cookie()}
        self.requests.post("http://182.92.178.83:8088/api/student/user/update", headers=headers, json=payload)
        # 查看个人信息接口
        result = self.requests.post("http://182.92.178.83:8088/api/student/user/current", headers=headers)
        act = result.json()["response"]["realName"]
        # 断言结果，返回的真实姓名是修改的姓名
        self.assertEqual(act, real_name)

    def test_005_log(self):
        """考试系统前台_查看用户动态"""
        # 先修改个人资料
        now_time = time.strftime("%Y%m%d%H%M%S", time.localtime(time.time()))
        real_name = "蔡坨坨" + now_time
        payload = {"id": 25261,
                   "userUuid": "aa1eeb04-f676-4a95-949c-6fe0a4eab85b",
                   "userName": "ctt01",
                   "realName": real_name,
                   "age": 12,
                   "role": 1,
                   "sex": 1,
                   "birthDay": "2020-12-07 00:00:00",
                   "phone": "15059224492",
                   "status": 1, "userLevel": 12,
                   "imagePath": ""}
        headers = {"Cookie": Student(self.requests).get_cookie()}
        self.requests.post("http://182.92.178.83:8088/api/student/user/update", headers=headers, json=payload)
        # 再调用查看动态接口，看是否有 ctt01 更新了个人资料
        result = self.requests.post("http://182.92.178.83:8088/api/student/user/log", headers=headers)
        print(result.json())
        ls = result.json()["response"]
        act = 123
        for l in range(0, len(ls)):
            if ls[l]["content"] == "ctt01 更新了个人资料":
                act = "ok"
        self.assertEqual("ok", act)


if __name__ == '__main__':
    unittest.main()
