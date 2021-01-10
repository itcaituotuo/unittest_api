import unittest
import requests
import time
from public.exam_public.teacher import Teacher


class TeacherCase(unittest.TestCase):
    def setUp(self):
        self.requests = requests

    def tearDown(self):
        pass

    def test_001_admin_login(self):
        """考试系统后台管理_管理员登录"""
        # 定义参数，用户名和密码，是否记住登录
        payload = {"userName": "admin", "password": "123456", "remember": False}
        result = self.requests.post("http://182.92.178.83:8088/api/user/login", json=payload)
        result_json = result.json()
        print(result_json)
        exp = "admin"
        try:
            act = result_json["response"]["userName"]
        except KeyError:  # 避免取不到key报错
            act = 666
        print(act)
        # 设置断言，返回结果中包含用户名
        self.assertEqual(exp, act)

    def test_002_insert_paper(self):
        """考试系统后台管理_添加试卷"""
        # ①添加试卷
        # 设置时间戳，用于保证试卷名唯一
        now_time = time.strftime("%Y%m%d%H%M%S", time.localtime(time.time()))
        # 试卷名
        paper_name = "测试" + now_time
        # 设置请求参数
        payload = {
            "level": 1,
            "subjectId": 1,
            "paperType": 1,
            "name": paper_name,
            "suggestTime": "60",
            "titleItems": [{
                "name": "题目标题" + now_time,
                "questionItems": [{
                    "id": 334,
                    "questionType": 1,
                    "subjectId": 1,
                    "title": "1+1",
                    "gradeLevel": 1,
                    "items": [{
                        "prefix": "A",
                        "content": "2",
                    },
                        {
                            "prefix": "B",
                            "content": "3",
                        },
                    ],
                    "analyze": "1+1=2",
                    "correct": "A",
                    "score": "10",
                    "difficult": 1,
                }]
            }]
        }
        # 调用get_cookie()方法，获取Cookie值
        headers = {"Cookie": Teacher(self.requests).get_cookie()}
        # 添加试卷接口
        self.requests.post("http://182.92.178.83:8088/api/admin/exam/paper/edit",
                           headers=headers,
                           json=payload)

        # ②查询所有试卷
        payload = {"id": "", "level": None, "subjectId": None, "pageIndex": 1, "pageSize": 10}
        headers = {"Cookie": Teacher(self.requests).get_cookie()}
        result = self.requests.post("http://182.92.178.83:8088/api/admin/exam/paper/page",
                                    headers=headers,
                                    json=payload)
        # 获取每套试卷的信息
        ls = result.json()["response"]["list"]
        exp = paper_name
        act = 666
        # 循环遍历取试卷名
        for l in ls:
            # 试卷名与新建试卷名一致，测试通过
            if l["name"] == exp:
                act = "ok"
                # 将试卷id取出，用于后续编辑试卷和删除试卷
                paper_id = l["id"]
                paper_id = str(paper_id)
        # 断言结果，查询到的试卷名与新建试卷名一致，说明新建成功，测试通过
        self.assertEqual(act, "ok")

        # ③编辑试卷
        now_time02 = time.strftime("%Y%m%d%H%M%S", time.localtime(time.time()))
        # 新试卷名
        paper_name02 = "新试卷名" + now_time02
        payload = {
            "id": paper_id,  # 传入paper_id
            "level": 1,
            "subjectId": 1,
            "paperType": 1,
            "name": paper_name02,
            "suggestTime": 60,
            "titleItems": [{
                "name": "题目标题20210110145245",
                "questionItems": [{
                    "id": 334,
                    "questionType": 1,
                    "subjectId": 1,
                    "title": "1+1",
                    "gradeLevel": 1,
                    "items": [{
                        "prefix": "A",
                        "content": "2",
                        "score": None
                    }, {
                        "prefix": "B",
                        "content": "3",
                        "score": None
                    }, {
                        "prefix": "C",
                        "content": "4",
                        "score": None
                    }, {
                        "prefix": "D",
                        "content": "5",
                        "score": None
                    }],
                    "analyze": "1+1=2",
                    "correctArray": None,
                    "correct": "A",
                    "score": "10",
                    "difficult": 1,
                    "itemOrder": 1
                }]
            }],
            "score": "10"
        }
        # 编辑试卷接口
        self.requests.post("http://182.92.178.83:8088/api/admin/exam/paper/edit",
                           headers=headers,
                           json=payload)
        # 查询试卷，判断是否编辑成功
        payload = {"id": "", "level": None, "subjectId": None, "pageIndex": 1, "pageSize": 10}
        headers = {"Cookie": Teacher(self.requests).get_cookie()}
        result = self.requests.post("http://182.92.178.83:8088/api/admin/exam/paper/page",
                                    headers=headers,
                                    json=payload)
        # print(result.json())
        # 获取每套试卷的信息
        ls = result.json()["response"]["list"]
        exp = paper_name02
        act = 666
        # 循环遍历取试卷名
        for l in ls:
            # 试卷名与新建试卷名一致，测试通过
            if l["name"] == exp:
                act = "ok"
        # 断言结果，查询到的试卷名是修改后的试卷名，说明编辑成功
        self.assertEqual("ok", act)

        # ④删除试卷
        # 调用delete_paper(paper_id)方法，删除试卷
        result = Teacher(self.requests).delete_paper(paper_id)
        exp = "成功"
        act = result.json()["message"]
        # 断言结果，返回信息message：成功，说明删除成功
        self.assertEqual(exp, act)

    def test_003_select_paper(self):
        """考试系统后台管理_查询试卷"""
        # 设置时间戳，用于保证试卷名唯一
        now_time = time.strftime("%Y%m%d%H%M%S", time.localtime(time.time()))
        # 试卷名
        paper_name = "测试" + now_time
        # 设置请求参数
        payload = {
            "level": 1,
            "subjectId": 1,
            "paperType": 1,
            "name": paper_name,
            "suggestTime": "60",
            "titleItems": [{
                "name": "题目标题" + now_time,
                "questionItems": [{
                    "id": 334,
                    "questionType": 1,
                    "subjectId": 1,
                    "title": "1+1",
                    "gradeLevel": 1,
                    "items": [{
                        "prefix": "A",
                        "content": "2",
                    },
                        {
                            "prefix": "B",
                            "content": "3",
                        },
                    ],
                    "analyze": "1+1=2",
                    "correct": "A",
                    "score": "10",
                    "difficult": 1,
                }]
            }]
        }
        # 调用get_cookie()方法，获取Cookie值
        headers = {"Cookie": Teacher(self.requests).get_cookie()}
        # 添加试卷接口
        self.requests.post("http://182.92.178.83:8088/api/admin/exam/paper/edit",
                           headers=headers,
                           json=payload)

        # 查询试卷
        payload = {"id": "", "level": None, "subjectId": None, "pageIndex": 1, "pageSize": 10}
        headers = {"Cookie": Teacher(self.requests).get_cookie()}
        result = self.requests.post("http://182.92.178.83:8088/api/admin/exam/paper/page",
                                    headers=headers,
                                    json=payload)
        # print(result.json())
        # 获取每套试卷的信息
        ls = result.json()["response"]["list"]
        exp = paper_name
        act = 666
        # 循环遍历取试卷名
        for l in ls:
            # 试卷名与新建试卷名一致，测试通过
            if l["name"] == exp:
                act = "ok"
                # 将试卷id取出，用于后续删除试卷
                paper_id = l["id"]
                paper_id = str(paper_id)
        # 断言结果
        self.assertEqual(act, "ok")

    def test_004_edit_paper(self):
        """考试系统后台管理_编辑试卷"""
        # ①先创建试卷
        # 设置时间戳，用于保证试卷名唯一
        now_time = time.strftime("%Y%m%d%H%M%S", time.localtime(time.time()))
        # 试卷名
        paper_name = "测试" + now_time
        # 设置请求参数
        payload = {
            "level": 1,
            "subjectId": 1,
            "paperType": 1,
            "name": paper_name,
            "suggestTime": "60",
            "titleItems": [{
                "name": "题目标题" + now_time,
                "questionItems": [{
                    "id": 334,
                    "questionType": 1,
                    "subjectId": 1,
                    "title": "1+1",
                    "gradeLevel": 1,
                    "items": [{
                        "prefix": "A",
                        "content": "2",
                    },
                        {
                            "prefix": "B",
                            "content": "3",
                        },
                    ],
                    "analyze": "1+1=2",
                    "correct": "A",
                    "score": "10",
                    "difficult": 1,
                }]
            }]
        }
        # 调用get_cookie()方法，获取Cookie值
        headers = {"Cookie": Teacher(self.requests).get_cookie()}
        # 添加试卷接口
        self.requests.post("http://182.92.178.83:8088/api/admin/exam/paper/edit",
                           headers=headers,
                           json=payload)

        # ②查询试卷，获取试卷的id
        payload = {"id": "", "level": None, "subjectId": None, "pageIndex": 1, "pageSize": 10}
        headers = {"Cookie": Teacher(self.requests).get_cookie()}
        result = self.requests.post("http://182.92.178.83:8088/api/admin/exam/paper/page",
                                    headers=headers,
                                    json=payload)
        # print(result.json())
        # 获取每套试卷的信息
        ls = result.json()["response"]["list"]
        exp = paper_name
        act = 666
        # 循环遍历取试卷名
        for l in ls:
            # 试卷名与新建试卷名一致，测试通过
            if l["name"] == exp:
                act = "ok"
                # 将试卷id取出，用于后续删除试卷
                paper_id = l["id"]
                paper_id = str(paper_id)

        # ③编辑试卷
        now_time02 = time.strftime("%Y%m%d%H%M%S", time.localtime(time.time()))
        # 新试卷名
        paper_name02 = "新试卷名" + now_time02
        payload = {
            "id": paper_id,  # 传入paper_id
            "level": 1,
            "subjectId": 1,
            "paperType": 1,
            "name": paper_name02,
            "suggestTime": 60,
            "titleItems": [{
                "name": "题目标题20210110145245",
                "questionItems": [{
                    "id": 334,
                    "questionType": 1,
                    "subjectId": 1,
                    "title": "1+1",
                    "gradeLevel": 1,
                    "items": [{
                        "prefix": "A",
                        "content": "2",
                        "score": None
                    }, {
                        "prefix": "B",
                        "content": "3",
                        "score": None
                    }, {
                        "prefix": "C",
                        "content": "4",
                        "score": None
                    }, {
                        "prefix": "D",
                        "content": "5",
                        "score": None
                    }],
                    "analyze": "1+1=2",
                    "correctArray": None,
                    "correct": "A",
                    "score": "10",
                    "difficult": 1,
                    "itemOrder": 1
                }]
            }],
            "score": "10"
        }
        result = self.requests.post("http://182.92.178.83:8088/api/admin/exam/paper/edit",
                                    headers=headers,
                                    json=payload)
        # ④查询试卷，判断是否编辑成功
        payload = {"id": "", "level": None, "subjectId": None, "pageIndex": 1, "pageSize": 10}
        headers = {"Cookie": Teacher(self.requests).get_cookie()}
        result = self.requests.post("http://182.92.178.83:8088/api/admin/exam/paper/page",
                                    headers=headers,
                                    json=payload)
        # print(result.json())
        # 获取每套试卷的信息
        ls = result.json()["response"]["list"]
        exp = paper_name02
        act = 666
        # 循环遍历取试卷名
        for l in ls:
            # 试卷名与新建试卷名一致，测试通过
            if l["name"] == exp:
                act = "ok"
        self.assertEqual("ok", act)

    def test_005_delete_paper(self):
        """考试系统后台管理_删除试卷"""
        # ①先创建试卷
        # 设置时间戳，用于保证试卷名唯一
        now_time = time.strftime("%Y%m%d%H%M%S", time.localtime(time.time()))
        # 试卷名
        paper_name = "测试" + now_time
        # 设置请求参数
        payload = {
            "level": 1,
            "subjectId": 1,
            "paperType": 1,
            "name": paper_name,
            "suggestTime": "60",
            "titleItems": [{
                "name": "题目标题" + now_time,
                "questionItems": [{
                    "id": 334,
                    "questionType": 1,
                    "subjectId": 1,
                    "title": "1+1",
                    "gradeLevel": 1,
                    "items": [{
                        "prefix": "A",
                        "content": "2",
                    },
                        {
                            "prefix": "B",
                            "content": "3",
                        },
                    ],
                    "analyze": "1+1=2",
                    "correct": "A",
                    "score": "10",
                    "difficult": 1,
                }]
            }]
        }
        # 调用get_cookie()方法，获取Cookie值
        headers = {"Cookie": Teacher(self.requests).get_cookie()}
        # 添加试卷接口
        self.requests.post("http://182.92.178.83:8088/api/admin/exam/paper/edit",
                           headers=headers,
                           json=payload)

        # ②查询试卷，获取试卷的id
        payload = {"id": "", "level": None, "subjectId": None, "pageIndex": 1, "pageSize": 10}
        headers = {"Cookie": Teacher(self.requests).get_cookie()}
        result = self.requests.post("http://182.92.178.83:8088/api/admin/exam/paper/page",
                                    headers=headers,
                                    json=payload)
        # print(result.json())
        # 获取每套试卷的信息
        ls = result.json()["response"]["list"]
        exp = paper_name
        act = 666
        # 循环遍历取试卷名
        for l in ls:
            # 试卷名与新建试卷名一致，测试通过
            if l["name"] == exp:
                act = "ok"
                # 将试卷id取出，用于后续删除试卷
                paper_id = l["id"]
                paper_id = str(paper_id)

        # ③根据试卷id删除试卷
        url_delete = "http://182.92.178.83:8088/api/admin/exam/paper/delete/" + paper_id
        print(url_delete)
        result = self.requests.post(url_delete, headers=headers)
        exp = "成功"
        act = result.json()["message"]
        # 断言结果
        self.assertEqual(exp, act)

    def test_006_insert_questions(self):
        """考试系统_添加题目"""
        # ①添加题目
        # 设置时间戳，用于保证试卷名唯一
        now_time = time.strftime("%Y%m%d%H%M%S", time.localtime(time.time()))
        # 试卷名
        question_title = "测试" + now_time
        # 设置请求参数
        payload = {
            "id": None,
            "questionType": 1,
            "gradeLevel": 4,
            "subjectId": 28,
            "title": question_title,
            "items": [{
                "prefix": "A",
                "content": "1"
            }, {
                "prefix": "B",
                "content": "2"
            }, {
                "prefix": "C",
                "content": "3"
            }, {
                "prefix": "D",
                "content": "4"
            }],
            "analyze": "测试解析",
            "correct": "C",
            "score": 100,
            "difficult": 5
        }
        # 调用get_cookie()方法，获取Cookie值
        headers = {"Cookie": Teacher(self.requests).get_cookie()}
        # 添加题目接口
        self.requests.post("http://182.92.178.83:8088/api/admin/question/edit",
                           headers=headers,
                           json=payload)

        # ②查询所有题目
        payload = {"id": None, "questionType": None, "level": None, "subjectId": None, "pageIndex": 1, "pageSize": 10}
        headers = {"Cookie": Teacher(self.requests).get_cookie()}
        result = self.requests.post("http://182.92.178.83:8088/api/admin/question/page",
                                    headers=headers,
                                    json=payload)
        # 获取每道题目的信息
        ls = result.json()["response"]["list"]
        act = 666
        # 循环遍历取试题目标题
        for l in range(0, len(ls)):
            # 如果查询到的题目标题与新建题目标题一致，测试通过
            if ls[l]["shortTitle"] == question_title:
                act = "ok"
                question_id = ls[l]["id"]
        # 断言结果，查询到的题目标题与新建题目标题一致，说明新建成功，测试通过
        self.assertEqual(act, "ok")

        # ③编辑题目
        now_time02 = time.strftime("%Y%m%d%H%M%S", time.localtime(time.time()))
        question_title02 = "新题目标题" + now_time02
        # 设置请求参数
        payload = {
            "id": question_id,
            "questionType": 1,
            "gradeLevel": 4,
            "subjectId": 28,
            "title": question_title02,
            "items": [{
                "prefix": "A",
                "content": "1"
            }, {
                "prefix": "B",
                "content": "2"
            }, {
                "prefix": "C",
                "content": "3"
            }, {
                "prefix": "D",
                "content": "4"
            }],
            "analyze": "测试解析",
            "correct": "C",
            "score": 100,
            "difficult": 5
        }
        # 编辑题目接口
        self.requests.post("http://182.92.178.83:8088/api/admin/question/edit",
                           headers=headers,
                           json=payload)
        # 获取每道题目的信息
        ls = result.json()["response"]["list"]
        act = 666
        # 循环遍历取试题目标题
        for l in range(0, len(ls)):
            # 如果查询到的题目标题与修改的题目标题一致，测试通过
            if ls[l]["shortTitle"] == question_title:
                act = "ok"
                question_id = ls[l]["id"]
        # 断言结果，查询到的题目标题与修改的题目标题一致，说明新建成功，测试通过
        self.assertEqual(act, "ok")

        # ④删除题目
        url_delete = "http://182.92.178.83:8088/api/admin/question/delete/" + str(question_id)
        result = self.requests.post(url_delete, headers=headers)
        exp = "成功"
        act = result.json()["message"]
        # 断言结果，返回信息message：成功，说明删除成功
        self.assertEqual(exp, act)

    def test_007_select_questions(self):
        """考试系统_查询所有题目"""
        # ①添加题目
        # 设置时间戳，用于保证试卷名唯一
        now_time = time.strftime("%Y%m%d%H%M%S", time.localtime(time.time()))
        # 试卷名
        question_title = "测试" + now_time
        # 设置请求参数
        payload = {
            "id": None,
            "questionType": 1,
            "gradeLevel": 4,
            "subjectId": 28,
            "title": question_title,
            "items": [{
                "prefix": "A",
                "content": "1"
            }, {
                "prefix": "B",
                "content": "2"
            }, {
                "prefix": "C",
                "content": "3"
            }, {
                "prefix": "D",
                "content": "4"
            }],
            "analyze": "测试解析",
            "correct": "C",
            "score": 100,
            "difficult": 5
        }
        # 调用get_cookie()方法，获取Cookie值
        headers = {"Cookie": Teacher(self.requests).get_cookie()}
        # 添加题目接口
        self.requests.post("http://182.92.178.83:8088/api/admin/question/edit",
                           headers=headers,
                           json=payload)

        # ②查询所有题目
        payload = {"id": None, "questionType": None, "level": None, "subjectId": None, "pageIndex": 1, "pageSize": 10}
        headers = {"Cookie": Teacher(self.requests).get_cookie()}
        result = self.requests.post("http://182.92.178.83:8088/api/admin/question/page",
                                    headers=headers,
                                    json=payload)
        # 获取每道题目的信息
        ls = result.json()["response"]["list"]
        act = 666
        # 循环遍历取试题目标题
        for l in range(0, len(ls)):
            # 如果查询到的题目标题与新建题目标题一致，测试通过
            if ls[l]["shortTitle"] == question_title:
                act = "ok"
                question_id = ls[l]["id"]
        # 断言结果，查询到的题目标题与新建题目标题一致，说明新建成功，测试通过
        self.assertEqual(act, "ok")

        # ③编辑题目
        now_time02 = time.strftime("%Y%m%d%H%M%S", time.localtime(time.time()))
        question_title02 = "新题目标题" + now_time02
        # 设置请求参数
        payload = {
            "id": question_id,
            "questionType": 1,
            "gradeLevel": 4,
            "subjectId": 28,
            "title": question_title02,
            "items": [{
                "prefix": "A",
                "content": "1"
            }, {
                "prefix": "B",
                "content": "2"
            }, {
                "prefix": "C",
                "content": "3"
            }, {
                "prefix": "D",
                "content": "4"
            }],
            "analyze": "测试解析",
            "correct": "C",
            "score": 100,
            "difficult": 5
        }
        # 编辑题目接口
        self.requests.post("http://182.92.178.83:8088/api/admin/question/edit",
                           headers=headers,
                           json=payload)
        # 获取每道题目的信息
        ls = result.json()["response"]["list"]
        act = 666
        # 循环遍历取试题目标题
        for l in range(0, len(ls)):
            # 如果查询到的题目标题与修改的题目标题一致，测试通过
            if ls[l]["shortTitle"] == question_title:
                act = "ok"
                question_id = ls[l]["id"]
        # 断言结果，查询到的题目标题与修改的题目标题一致，说明新建成功，测试通过
        self.assertEqual(act, "ok")

        # ④删除题目
        url_delete = "http://182.92.178.83:8088/api/admin/question/delete/" + str(question_id)
        result = self.requests.post(url_delete, headers=headers)
        exp = "成功"
        act = result.json()["message"]
        # 断言结果，返回信息message：成功，说明删除成功
        self.assertEqual(exp, act)

    def test_008_update_questions(self):
        """考试系统_编辑题目"""
        # ①添加题目
        # 设置时间戳，用于保证试卷名唯一
        now_time = time.strftime("%Y%m%d%H%M%S", time.localtime(time.time()))
        # 试卷名
        question_title = "测试" + now_time
        # 设置请求参数
        payload = {
            "id": None,
            "questionType": 1,
            "gradeLevel": 4,
            "subjectId": 28,
            "title": question_title,
            "items": [{
                "prefix": "A",
                "content": "1"
            }, {
                "prefix": "B",
                "content": "2"
            }, {
                "prefix": "C",
                "content": "3"
            }, {
                "prefix": "D",
                "content": "4"
            }],
            "analyze": "测试解析",
            "correct": "C",
            "score": 100,
            "difficult": 5
        }
        # 调用get_cookie()方法，获取Cookie值
        headers = {"Cookie": Teacher(self.requests).get_cookie()}
        # 添加题目接口
        self.requests.post("http://182.92.178.83:8088/api/admin/question/edit",
                           headers=headers,
                           json=payload)

        # ②查询所有题目
        payload = {"id": None, "questionType": None, "level": None, "subjectId": None, "pageIndex": 1, "pageSize": 10}
        headers = {"Cookie": Teacher(self.requests).get_cookie()}
        result = self.requests.post("http://182.92.178.83:8088/api/admin/question/page",
                                    headers=headers,
                                    json=payload)
        # 获取每道题目的信息
        ls = result.json()["response"]["list"]
        act = 666
        # 循环遍历取试题目标题
        for l in range(0, len(ls)):
            # 如果查询到的题目标题与新建题目标题一致，测试通过
            if ls[l]["shortTitle"] == question_title:
                act = "ok"
                question_id = ls[l]["id"]
        # 断言结果，查询到的题目标题与新建题目标题一致，说明新建成功，测试通过
        self.assertEqual(act, "ok")

        # ③编辑题目
        now_time02 = time.strftime("%Y%m%d%H%M%S", time.localtime(time.time()))
        question_title02 = "新题目标题" + now_time02
        # 设置请求参数
        payload = {
            "id": question_id,
            "questionType": 1,
            "gradeLevel": 4,
            "subjectId": 28,
            "title": question_title02,
            "items": [{
                "prefix": "A",
                "content": "1"
            }, {
                "prefix": "B",
                "content": "2"
            }, {
                "prefix": "C",
                "content": "3"
            }, {
                "prefix": "D",
                "content": "4"
            }],
            "analyze": "测试解析",
            "correct": "C",
            "score": 100,
            "difficult": 5
        }
        # 编辑题目接口
        self.requests.post("http://182.92.178.83:8088/api/admin/question/edit",
                           headers=headers,
                           json=payload)
        # 获取每道题目的信息
        ls = result.json()["response"]["list"]
        act = 666
        # 循环遍历取试题目标题
        for l in range(0, len(ls)):
            # 如果查询到的题目标题与修改的题目标题一致，测试通过
            if ls[l]["shortTitle"] == question_title:
                act = "ok"
                question_id = ls[l]["id"]
        # 断言结果，查询到的题目标题与修改的题目标题一致，说明新建成功，测试通过
        self.assertEqual(act, "ok")

        # ④删除题目
        url_delete = "http://182.92.178.83:8088/api/admin/question/delete/" + str(question_id)
        result = self.requests.post(url_delete, headers=headers)
        exp = "成功"
        act = result.json()["message"]
        # 断言结果，返回信息message：成功，说明删除成功
        self.assertEqual(exp, act)

    def test_009_delete_questions(self):
        """考试系统_删除题目"""
        # ①添加题目
        # 设置时间戳，用于保证试卷名唯一
        now_time = time.strftime("%Y%m%d%H%M%S", time.localtime(time.time()))
        # 试卷名
        question_title = "测试" + now_time
        # 设置请求参数
        payload = {
            "id": None,
            "questionType": 1,
            "gradeLevel": 4,
            "subjectId": 28,
            "title": question_title,
            "items": [{
                "prefix": "A",
                "content": "1"
            }, {
                "prefix": "B",
                "content": "2"
            }, {
                "prefix": "C",
                "content": "3"
            }, {
                "prefix": "D",
                "content": "4"
            }],
            "analyze": "测试解析",
            "correct": "C",
            "score": 100,
            "difficult": 5
        }
        # 调用get_cookie()方法，获取Cookie值
        headers = {"Cookie": Teacher(self.requests).get_cookie()}
        # 添加题目接口
        self.requests.post("http://182.92.178.83:8088/api/admin/question/edit",
                           headers=headers,
                           json=payload)

        # ②查询所有题目
        payload = {"id": None, "questionType": None, "level": None, "subjectId": None, "pageIndex": 1, "pageSize": 10}
        headers = {"Cookie": Teacher(self.requests).get_cookie()}
        result = self.requests.post("http://182.92.178.83:8088/api/admin/question/page",
                                    headers=headers,
                                    json=payload)
        # 获取每道题目的信息
        ls = result.json()["response"]["list"]
        act = 666
        # 循环遍历取试题目标题
        for l in range(0, len(ls)):
            # 如果查询到的题目标题与新建题目标题一致，测试通过
            if ls[l]["shortTitle"] == question_title:
                act = "ok"
                question_id = ls[l]["id"]
        # 断言结果，查询到的题目标题与新建题目标题一致，说明新建成功，测试通过
        self.assertEqual(act, "ok")

        # ③编辑题目
        now_time02 = time.strftime("%Y%m%d%H%M%S", time.localtime(time.time()))
        question_title02 = "新题目标题" + now_time02
        # 设置请求参数
        payload = {
            "id": question_id,
            "questionType": 1,
            "gradeLevel": 4,
            "subjectId": 28,
            "title": question_title02,
            "items": [{
                "prefix": "A",
                "content": "1"
            }, {
                "prefix": "B",
                "content": "2"
            }, {
                "prefix": "C",
                "content": "3"
            }, {
                "prefix": "D",
                "content": "4"
            }],
            "analyze": "测试解析",
            "correct": "C",
            "score": 100,
            "difficult": 5
        }
        # 编辑题目接口
        self.requests.post("http://182.92.178.83:8088/api/admin/question/edit",
                           headers=headers,
                           json=payload)
        # 获取每道题目的信息
        ls = result.json()["response"]["list"]
        act = 666
        # 循环遍历取试题目标题
        for l in range(0, len(ls)):
            # 如果查询到的题目标题与修改的题目标题一致，测试通过
            if ls[l]["shortTitle"] == question_title:
                act = "ok"
                question_id = ls[l]["id"]
        # 断言结果，查询到的题目标题与修改的题目标题一致，说明新建成功，测试通过
        self.assertEqual(act, "ok")

        # ④删除题目
        url_delete = "http://182.92.178.83:8088/api/admin/question/delete/" + str(question_id)
        result = self.requests.post(url_delete, headers=headers)
        exp = "成功"
        act = result.json()["message"]
        # 断言结果，返回信息message：成功，说明删除成功
        self.assertEqual(exp, act)


if __name__ == '__main__':
    unittest.main()
