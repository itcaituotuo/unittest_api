import unittest
import requests
from public.vblog_public.index import VBlog
import time


class VBlogCase(unittest.TestCase):
    def setUp(self):
        self.requests = requests

    def tearDown(self):
        pass

    def test_001_login(self):
        """V部落_用户登录"""
        url_v_login = "http://182.92.178.83:8081/login"
        # 定义参数，字典格式
        payload = {'username': 'sang', 'password': '123'}
        # Content-Type: application/json --> json
        # Content-Type: application/x-www-form-urlencoded --> data
        result = requests.post(url_v_login, data=payload)
        # 将返回结果转为json格式
        result_json = result.json()
        # 断言结果，响应结果返回 登录成功
        self.assertEqual("登录成功", result_json["msg"])

    def test_002_insert_article(self):
        """V部落_新增文章"""
        now_time = time.strftime("%Y%m%d%H%M%S", time.localtime(time.time()))
        title = "蔡坨坨" + now_time
        payload = {"id": -1, "title": title, "mdContent": "文章内容", "state": 1, "htmlContent": "<p>文章内容</p>",
                   "dynamicTags": "", "cid": 62}
        headers = {"Cookie": VBlog(self.requests).get_cookie()}
        result = self.requests.post("http://182.92.178.83:8081/article/", headers=headers, data=payload)

        # 查询文章
        url_v_article = "http://182.92.178.83:8081/article/all"
        article_params = {"state": 1,  # -1：全部文章 1：已发表 0：回收站 2：草稿箱
                          "page": 1,  # 显示第1页
                          "count": 6,  # 每页显示6条
                          "keywords": title  # 包含的关键字title
                          }
        result = requests.get(url_v_article, headers=headers, params=article_params, timeout=30)
        print(result.json())  # 响应结果以json的形式打印输出
        ls = result.json()["articles"]
        act = 123
        # 查到新增的文章，说明新增成功
        for l in range(0, len(ls)):
            if ls[l]["title"] == title:
                act = "ok"
                article_id = ls[l]["id"]
        self.assertEqual("ok", act)

        # 编辑文章
        now_time = time.strftime("%Y%m%d%H%M%S", time.localtime(time.time()))
        title = "修改文章" + now_time
        payload = {"id": article_id, "title": title, "mdContent": "修改内容", "state": 1, "htmlContent": "<p>修改内容</p>",
                   "dynamicTags": "", "cid": 62}
        headers = {"Cookie": VBlog(self.requests).get_cookie()}
        self.requests.post("http://182.92.178.83:8081/article/", headers=headers, data=payload)
        # 编辑完，查询文章
        url_v_article = "http://182.92.178.83:8081/article/all"
        article_params = {"state": 1,  # -1：全部文章 1：已发表 0：回收站 2：草稿箱
                          "page": 1,  # 显示第1页
                          "count": 6,  # 每页显示6条
                          "keywords": title  # 包含的关键字title
                          }
        result = requests.get(url_v_article, headers=headers, params=article_params, timeout=30)
        print(result.json())  # 响应结果以json的形式打印输出
        ls = result.json()["articles"]
        act = 123
        # 查到新增的文章，说明新增成功
        for l in range(0, len(ls)):
            if ls[l]["title"] == title:
                act = "ok"
                article_id = ls[l]["id"]
        self.assertEqual("ok", act)

        # 查看文章详情
        article_id = str(article_id)
        result = self.requests.get("http://182.92.178.83:8081/article/" + article_id, headers=headers)
        print(result.json())
        if result.json()["title"] == title:
            act = "ok"
        self.assertEqual(act, "ok")

        # 删除文章
        payload = {'aids': article_id, 'state': 1}
        result = self.requests.put("http://182.92.178.83:8081/article/dustbin", headers=headers, data=payload)
        print(result.json())
        act = result.json()["msg"]
        self.assertEqual(act, "删除成功!")

    def test_003_select_article(self):
        """V部落_查询文章"""
        now_time = time.strftime("%Y%m%d%H%M%S", time.localtime(time.time()))
        title = "蔡坨坨" + now_time
        payload = {"id": -1, "title": title, "mdContent": "文章内容", "state": 1, "htmlContent": "<p>文章内容</p>",
                   "dynamicTags": "", "cid": 62}
        headers = {"Cookie": VBlog(self.requests).get_cookie()}
        result = self.requests.post("http://182.92.178.83:8081/article/", headers=headers, data=payload)

        # 查询文章
        url_v_article = "http://182.92.178.83:8081/article/all"
        article_params = {"state": 1,  # -1：全部文章 1：已发表 0：回收站 2：草稿箱
                          "page": 1,  # 显示第1页
                          "count": 6,  # 每页显示6条
                          "keywords": title  # 包含的关键字title
                          }
        result = requests.get(url_v_article, headers=headers, params=article_params, timeout=30)
        print(result.json())  # 响应结果以json的形式打印输出
        ls = result.json()["articles"]
        act = 123
        # 查到新增的文章，说明新增成功
        for l in range(0, len(ls)):
            if ls[l]["title"] == title:
                act = "ok"
                article_id = ls[l]["id"]
        self.assertEqual("ok", act)

        # 编辑文章
        now_time = time.strftime("%Y%m%d%H%M%S", time.localtime(time.time()))
        title = "修改文章" + now_time
        payload = {"id": article_id, "title": title, "mdContent": "修改内容", "state": 1, "htmlContent": "<p>修改内容</p>",
                   "dynamicTags": "", "cid": 62}
        headers = {"Cookie": VBlog(self.requests).get_cookie()}
        self.requests.post("http://182.92.178.83:8081/article/", headers=headers, data=payload)
        # 编辑完，查询文章
        url_v_article = "http://182.92.178.83:8081/article/all"
        article_params = {"state": 1,  # -1：全部文章 1：已发表 0：回收站 2：草稿箱
                          "page": 1,  # 显示第1页
                          "count": 6,  # 每页显示6条
                          "keywords": title  # 包含的关键字title
                          }
        result = requests.get(url_v_article, headers=headers, params=article_params, timeout=30)
        print(result.json())  # 响应结果以json的形式打印输出
        ls = result.json()["articles"]
        act = 123
        # 查到新增的文章，说明新增成功
        for l in range(0, len(ls)):
            if ls[l]["title"] == title:
                act = "ok"
                article_id = ls[l]["id"]
        self.assertEqual("ok", act)

        # 查看文章详情
        article_id = str(article_id)
        result = self.requests.get("http://182.92.178.83:8081/article/" + article_id, headers=headers)
        print(result.json())
        if result.json()["title"] == title:
            act = "ok"
        self.assertEqual(act, "ok")

        # 删除文章
        payload = {'aids': article_id, 'state': 1}
        result = self.requests.put("http://182.92.178.83:8081/article/dustbin", headers=headers, data=payload)
        print(result.json())
        act = result.json()["msg"]
        self.assertEqual(act, "删除成功!")

    def test_004_update_article(self):
        """V部落_编辑文章"""
        now_time = time.strftime("%Y%m%d%H%M%S", time.localtime(time.time()))
        title = "蔡坨坨" + now_time
        payload = {"id": -1, "title": title, "mdContent": "文章内容", "state": 1, "htmlContent": "<p>文章内容</p>",
                   "dynamicTags": "", "cid": 62}
        headers = {"Cookie": VBlog(self.requests).get_cookie()}
        result = self.requests.post("http://182.92.178.83:8081/article/", headers=headers, data=payload)

        # 查询文章
        url_v_article = "http://182.92.178.83:8081/article/all"
        article_params = {"state": 1,  # -1：全部文章 1：已发表 0：回收站 2：草稿箱
                          "page": 1,  # 显示第1页
                          "count": 6,  # 每页显示6条
                          "keywords": title  # 包含的关键字title
                          }
        result = requests.get(url_v_article, headers=headers, params=article_params, timeout=30)
        print(result.json())  # 响应结果以json的形式打印输出
        ls = result.json()["articles"]
        act = 123
        # 查到新增的文章，说明新增成功
        for l in range(0, len(ls)):
            if ls[l]["title"] == title:
                act = "ok"
                article_id = ls[l]["id"]
        self.assertEqual("ok", act)

        # 编辑文章
        now_time = time.strftime("%Y%m%d%H%M%S", time.localtime(time.time()))
        title = "修改文章" + now_time
        payload = {"id": article_id, "title": title, "mdContent": "修改内容", "state": 1, "htmlContent": "<p>修改内容</p>",
                   "dynamicTags": "", "cid": 62}
        headers = {"Cookie": VBlog(self.requests).get_cookie()}
        self.requests.post("http://182.92.178.83:8081/article/", headers=headers, data=payload)
        # 编辑完，查询文章
        url_v_article = "http://182.92.178.83:8081/article/all"
        article_params = {"state": 1,  # -1：全部文章 1：已发表 0：回收站 2：草稿箱
                          "page": 1,  # 显示第1页
                          "count": 6,  # 每页显示6条
                          "keywords": title  # 包含的关键字title
                          }
        result = requests.get(url_v_article, headers=headers, params=article_params, timeout=30)
        print(result.json())  # 响应结果以json的形式打印输出
        ls = result.json()["articles"]
        act = 123
        # 查到新增的文章，说明新增成功
        for l in range(0, len(ls)):
            if ls[l]["title"] == title:
                act = "ok"
                article_id = ls[l]["id"]
        self.assertEqual("ok", act)

        # 查看文章详情
        article_id = str(article_id)
        result = self.requests.get("http://182.92.178.83:8081/article/" + article_id, headers=headers)
        print(result.json())
        if result.json()["title"] == title:
            act = "ok"
        self.assertEqual(act, "ok")

        # 删除文章
        payload = {'aids': article_id, 'state': 1}
        result = self.requests.put("http://182.92.178.83:8081/article/dustbin", headers=headers, data=payload)
        print(result.json())
        act = result.json()["msg"]
        self.assertEqual(act, "删除成功!")

    def test_005_detail_article(self):
        """V部落_查看文章详情"""
        now_time = time.strftime("%Y%m%d%H%M%S", time.localtime(time.time()))
        title = "蔡坨坨" + now_time
        payload = {"id": -1, "title": title, "mdContent": "文章内容", "state": 1, "htmlContent": "<p>文章内容</p>",
                   "dynamicTags": "", "cid": 62}
        headers = {"Cookie": VBlog(self.requests).get_cookie()}
        result = self.requests.post("http://182.92.178.83:8081/article/", headers=headers, data=payload)

        # 查询文章
        url_v_article = "http://182.92.178.83:8081/article/all"
        article_params = {"state": 1,  # -1：全部文章 1：已发表 0：回收站 2：草稿箱
                          "page": 1,  # 显示第1页
                          "count": 6,  # 每页显示6条
                          "keywords": title  # 包含的关键字title
                          }
        result = requests.get(url_v_article, headers=headers, params=article_params, timeout=30)
        print(result.json())  # 响应结果以json的形式打印输出
        ls = result.json()["articles"]
        act = 123
        # 查到新增的文章，说明新增成功
        for l in range(0, len(ls)):
            if ls[l]["title"] == title:
                act = "ok"
                article_id = ls[l]["id"]
        self.assertEqual("ok", act)

        # 编辑文章
        now_time = time.strftime("%Y%m%d%H%M%S", time.localtime(time.time()))
        title = "修改文章" + now_time
        payload = {"id": article_id, "title": title, "mdContent": "修改内容", "state": 1, "htmlContent": "<p>修改内容</p>",
                   "dynamicTags": "", "cid": 62}
        headers = {"Cookie": VBlog(self.requests).get_cookie()}
        self.requests.post("http://182.92.178.83:8081/article/", headers=headers, data=payload)
        # 编辑完，查询文章
        url_v_article = "http://182.92.178.83:8081/article/all"
        article_params = {"state": 1,  # -1：全部文章 1：已发表 0：回收站 2：草稿箱
                          "page": 1,  # 显示第1页
                          "count": 6,  # 每页显示6条
                          "keywords": title  # 包含的关键字title
                          }
        result = requests.get(url_v_article, headers=headers, params=article_params, timeout=30)
        print(result.json())  # 响应结果以json的形式打印输出
        ls = result.json()["articles"]
        act = 123
        # 查到新增的文章，说明新增成功
        for l in range(0, len(ls)):
            if ls[l]["title"] == title:
                act = "ok"
                article_id = ls[l]["id"]
        self.assertEqual("ok", act)

        # 查看文章详情
        article_id = str(article_id)
        result = self.requests.get("http://182.92.178.83:8081/article/" + article_id, headers=headers)
        print(result.json())
        if result.json()["title"] == title:
            act = "ok"
        self.assertEqual(act, "ok")

        # 删除文章
        payload = {'aids': article_id, 'state': 1}
        result = self.requests.put("http://182.92.178.83:8081/article/dustbin", headers=headers, data=payload)
        print(result.json())
        act = result.json()["msg"]
        self.assertEqual(act, "删除成功!")

    def test_006_delete_article(self):
        """V部落_删除文章"""
        now_time = time.strftime("%Y%m%d%H%M%S", time.localtime(time.time()))
        title = "蔡坨坨" + now_time
        payload = {"id": -1, "title": title, "mdContent": "文章内容", "state": 1, "htmlContent": "<p>文章内容</p>",
                   "dynamicTags": "", "cid": 62}
        headers = {"Cookie": VBlog(self.requests).get_cookie()}
        self.requests.post("http://182.92.178.83:8081/article/", headers=headers, data=payload)

        # 查询文章
        url_v_article = "http://182.92.178.83:8081/article/all"
        article_params = {"state": 1,  # -1：全部文章 1：已发表 0：回收站 2：草稿箱
                          "page": 1,  # 显示第1页
                          "count": 6,  # 每页显示6条
                          "keywords": title  # 包含的关键字title
                          }
        result = requests.get(url_v_article, headers=headers, params=article_params, timeout=30)
        print(result.json())  # 响应结果以json的形式打印输出
        ls = result.json()["articles"]
        act = 123
        # 查到新增的文章，说明新增成功
        for l in range(0, len(ls)):
            if ls[l]["title"] == title:
                act = "ok"
                article_id = ls[l]["id"]
        self.assertEqual("ok", act)

        # 编辑文章
        now_time = time.strftime("%Y%m%d%H%M%S", time.localtime(time.time()))
        title = "修改文章" + now_time
        payload = {"id": article_id, "title": title, "mdContent": "修改内容", "state": 1, "htmlContent": "<p>修改内容</p>",
                   "dynamicTags": "", "cid": 62}
        headers = {"Cookie": VBlog(self.requests).get_cookie()}
        self.requests.post("http://182.92.178.83:8081/article/", headers=headers, data=payload)
        # 编辑完，查询文章
        url_v_article = "http://182.92.178.83:8081/article/all"
        article_params = {"state": 1,  # -1：全部文章 1：已发表 0：回收站 2：草稿箱
                          "page": 1,  # 显示第1页
                          "count": 6,  # 每页显示6条
                          "keywords": title  # 包含的关键字title
                          }
        result = requests.get(url_v_article, headers=headers, params=article_params, timeout=30)
        print(result.json())  # 响应结果以json的形式打印输出
        ls = result.json()["articles"]
        act = 123
        # 查到新增的文章，说明新增成功
        for l in range(0, len(ls)):
            if ls[l]["title"] == title:
                act = "ok"
                article_id = ls[l]["id"]
        self.assertEqual("ok", act)

        # 查看文章详情
        article_id = str(article_id)
        result = self.requests.get("http://182.92.178.83:8081/article/" + article_id, headers=headers)
        print(result.json())
        if result.json()["title"] == title:
            act = "ok"
        self.assertEqual(act, "ok")

        # 删除文章
        payload = {'aids': article_id, 'state': 1}
        result = self.requests.put("http://182.92.178.83:8081/article/dustbin", headers=headers, data=payload)
        print(result.json())
        act = result.json()["msg"]
        self.assertEqual(act, "删除成功!")

    def test_007_insert_category(self):
        """V部落_新增栏目"""
        now_time = time.strftime("%Y%m%d%H%M%S", time.localtime(time.time()))
        category_name = "蔡坨坨栏目" + now_time
        payload = {"cateName": category_name}
        headers = {"Cookie": VBlog(self.requests).get_cookie()}
        result = self.requests.post("http://182.92.178.83:8081/admin/category/", headers=headers, data=payload)
        print(result.json())  # {'status': 'success', 'msg': '添加成功!'}
        self.assertEqual("添加成功!", result.json()["msg"])

        # 查询所有栏目
        result = self.requests.get("http://182.92.178.83:8081/admin/category/all", headers=headers)
        act = 666
        # 查询到刚新增的栏目的栏目名，说明查询成功
        for l in range(0, len(result.json())):
            if result.json()[l]["cateName"] == category_name:
                act = "ok"
                category_id = result.json()[l]["id"]
        self.assertEqual(act, "ok")

        # 编辑栏目
        new_now_time = time.strftime("%Y%m%d%H%M%S", time.localtime(time.time()))
        new_category_name = "更新栏目" + new_now_time
        payload = {"id": category_id, "cateName": new_category_name}
        result = self.requests.put("http://182.92.178.83:8081/admin/category/", headers=headers, data=payload)
        print(result.json())  # {'status': 'success', 'msg': '修改成功!'}
        self.assertEqual("修改成功!", result.json()["msg"])

        # 删除栏目
        result = self.requests.delete("http://182.92.178.83:8081/admin/category/" + str(category_id), headers=headers)
        print(result.json())  # {'status': 'success', 'msg': '删除成功!'}
        self.assertEqual("删除成功!", result.json()["msg"])

        # 批量删除
        # 先新建多个栏目
        now_time = time.strftime("%Y%m%d%H%M%S", time.localtime(time.time()))
        category_name_01 = "蔡坨坨栏目" + now_time
        payload = {"cateName": category_name_01}
        headers = {"Cookie": VBlog(self.requests).get_cookie()}
        result = self.requests.post("http://182.92.178.83:8081/admin/category/", headers=headers, data=payload)
        print(result.json())  # {'status': 'success', 'msg': '添加成功!'}
        # 查询所有栏目，取栏目id
        result = self.requests.get("http://182.92.178.83:8081/admin/category/all", headers=headers)
        for l in range(0, len(result.json())):
            if result.json()[l]["cateName"] == category_name_01:
                category_id_01 = result.json()[l]["id"]

        # 先新建多个栏目
        now_time = time.strftime("%Y%m%d%H%M%S", time.localtime(time.time()))
        category_name_02 = "蔡坨坨栏目" + now_time
        payload = {"cateName": category_name_02}
        headers = {"Cookie": VBlog(self.requests).get_cookie()}
        result = self.requests.post("http://182.92.178.83:8081/admin/category/", headers=headers, data=payload)
        print(result.json())  # {'status': 'success', 'msg': '添加成功!'}
        # 查询所有栏目，取栏目id
        result = self.requests.get("http://182.92.178.83:8081/admin/category/all", headers=headers)
        for l in range(0, len(result.json())):
            if result.json()[l]["cateName"] == category_name_02:
                category_id_02 = result.json()[l]["id"]

        result = self.requests.delete(
            "http://182.92.178.83:8081/admin/category/" + str(category_id_01) + "," + str(category_id_02),
            headers=headers)
        print(result.json())  # {'status': 'success', 'msg': '删除成功!'}
        self.assertEqual("删除成功!", result.json()["msg"])

    def test_008_select_category(self):
        """V部落_查询所有栏目"""
        now_time = time.strftime("%Y%m%d%H%M%S", time.localtime(time.time()))
        category_name = "蔡坨坨栏目" + now_time
        payload = {"cateName": category_name}
        headers = {"Cookie": VBlog(self.requests).get_cookie()}
        result = self.requests.post("http://182.92.178.83:8081/admin/category/", headers=headers, data=payload)
        print(result.json())  # {'status': 'success', 'msg': '添加成功!'}
        self.assertEqual("添加成功!", result.json()["msg"])

        # 查询所有栏目
        result = self.requests.get("http://182.92.178.83:8081/admin/category/all", headers=headers)
        act = 666
        # 查询到刚新增的栏目的栏目名，说明查询成功
        for l in range(0, len(result.json())):
            if result.json()[l]["cateName"] == category_name:
                act = "ok"
                category_id = result.json()[l]["id"]
        self.assertEqual(act, "ok")

        # 编辑栏目
        new_now_time = time.strftime("%Y%m%d%H%M%S", time.localtime(time.time()))
        new_category_name = "更新栏目" + new_now_time
        payload = {"id": category_id, "cateName": new_category_name}
        result = self.requests.put("http://182.92.178.83:8081/admin/category/", headers=headers, data=payload)
        print(result.json())  # {'status': 'success', 'msg': '修改成功!'}
        self.assertEqual("修改成功!", result.json()["msg"])

        # 删除栏目
        result = self.requests.delete("http://182.92.178.83:8081/admin/category/" + str(category_id), headers=headers)
        print(result.json())  # {'status': 'success', 'msg': '删除成功!'}
        self.assertEqual("删除成功!", result.json()["msg"])

        # 批量删除
        # 先新建多个栏目
        now_time = time.strftime("%Y%m%d%H%M%S", time.localtime(time.time()))
        category_name_01 = "蔡坨坨栏目" + now_time
        payload = {"cateName": category_name_01}
        headers = {"Cookie": VBlog(self.requests).get_cookie()}
        result = self.requests.post("http://182.92.178.83:8081/admin/category/", headers=headers, data=payload)
        print(result.json())  # {'status': 'success', 'msg': '添加成功!'}
        # 查询所有栏目，取栏目id
        result = self.requests.get("http://182.92.178.83:8081/admin/category/all", headers=headers)
        for l in range(0, len(result.json())):
            if result.json()[l]["cateName"] == category_name_01:
                category_id_01 = result.json()[l]["id"]

        # 先新建多个栏目
        now_time = time.strftime("%Y%m%d%H%M%S", time.localtime(time.time()))
        category_name_02 = "蔡坨坨栏目" + now_time
        payload = {"cateName": category_name_02}
        headers = {"Cookie": VBlog(self.requests).get_cookie()}
        result = self.requests.post("http://182.92.178.83:8081/admin/category/", headers=headers, data=payload)
        print(result.json())  # {'status': 'success', 'msg': '添加成功!'}
        # 查询所有栏目，取栏目id
        result = self.requests.get("http://182.92.178.83:8081/admin/category/all", headers=headers)
        for l in range(0, len(result.json())):
            if result.json()[l]["cateName"] == category_name_02:
                category_id_02 = result.json()[l]["id"]

        result = self.requests.delete(
            "http://182.92.178.83:8081/admin/category/" + str(category_id_01) + "," + str(category_id_02),
            headers=headers)
        print(result.json())  # {'status': 'success', 'msg': '删除成功!'}
        self.assertEqual("删除成功!", result.json()["msg"])

    def test_009_update_category(self):
        """V部落_编辑栏目"""
        now_time = time.strftime("%Y%m%d%H%M%S", time.localtime(time.time()))
        category_name = "蔡坨坨栏目" + now_time
        payload = {"cateName": category_name}
        headers = {"Cookie": VBlog(self.requests).get_cookie()}
        result = self.requests.post("http://182.92.178.83:8081/admin/category/", headers=headers, data=payload)
        print(result.json())  # {'status': 'success', 'msg': '添加成功!'}
        self.assertEqual("添加成功!", result.json()["msg"])

        # 查询所有栏目
        result = self.requests.get("http://182.92.178.83:8081/admin/category/all", headers=headers)
        act = 666
        # 查询到刚新增的栏目的栏目名，说明查询成功
        for l in range(0, len(result.json())):
            if result.json()[l]["cateName"] == category_name:
                act = "ok"
                category_id = result.json()[l]["id"]
        self.assertEqual(act, "ok")

        # 编辑栏目
        new_now_time = time.strftime("%Y%m%d%H%M%S", time.localtime(time.time()))
        new_category_name = "更新栏目" + new_now_time
        payload = {"id": category_id, "cateName": new_category_name}
        result = self.requests.put("http://182.92.178.83:8081/admin/category/", headers=headers, data=payload)
        print(result.json())  # {'status': 'success', 'msg': '修改成功!'}
        self.assertEqual("修改成功!", result.json()["msg"])

        # 删除栏目
        result = self.requests.delete("http://182.92.178.83:8081/admin/category/" + str(category_id), headers=headers)
        print(result.json())  # {'status': 'success', 'msg': '删除成功!'}
        self.assertEqual("删除成功!", result.json()["msg"])

        # 批量删除
        # 先新建多个栏目
        now_time = time.strftime("%Y%m%d%H%M%S", time.localtime(time.time()))
        category_name_01 = "蔡坨坨栏目" + now_time
        payload = {"cateName": category_name_01}
        headers = {"Cookie": VBlog(self.requests).get_cookie()}
        result = self.requests.post("http://182.92.178.83:8081/admin/category/", headers=headers, data=payload)
        print(result.json())  # {'status': 'success', 'msg': '添加成功!'}
        # 查询所有栏目，取栏目id
        result = self.requests.get("http://182.92.178.83:8081/admin/category/all", headers=headers)
        for l in range(0, len(result.json())):
            if result.json()[l]["cateName"] == category_name_01:
                category_id_01 = result.json()[l]["id"]

        # 先新建多个栏目
        now_time = time.strftime("%Y%m%d%H%M%S", time.localtime(time.time()))
        category_name_02 = "蔡坨坨栏目" + now_time
        payload = {"cateName": category_name_02}
        headers = {"Cookie": VBlog(self.requests).get_cookie()}
        result = self.requests.post("http://182.92.178.83:8081/admin/category/", headers=headers, data=payload)
        print(result.json())  # {'status': 'success', 'msg': '添加成功!'}
        # 查询所有栏目，取栏目id
        result = self.requests.get("http://182.92.178.83:8081/admin/category/all", headers=headers)
        for l in range(0, len(result.json())):
            if result.json()[l]["cateName"] == category_name_02:
                category_id_02 = result.json()[l]["id"]

        result = self.requests.delete(
            "http://182.92.178.83:8081/admin/category/" + str(category_id_01) + "," + str(category_id_02),
            headers=headers)
        print(result.json())  # {'status': 'success', 'msg': '删除成功!'}
        self.assertEqual("删除成功!", result.json()["msg"])

    def test_010_delete_category(self):
        """V部落_删除栏目"""
        now_time = time.strftime("%Y%m%d%H%M%S", time.localtime(time.time()))
        category_name = "蔡坨坨栏目" + now_time
        payload = {"cateName": category_name}
        headers = {"Cookie": VBlog(self.requests).get_cookie()}
        result = self.requests.post("http://182.92.178.83:8081/admin/category/", headers=headers, data=payload)
        print(result.json())  # {'status': 'success', 'msg': '添加成功!'}
        self.assertEqual("添加成功!", result.json()["msg"])

        # 查询所有栏目
        result = self.requests.get("http://182.92.178.83:8081/admin/category/all", headers=headers)
        act = 666
        # 查询到刚新增的栏目的栏目名，说明查询成功
        for l in range(0, len(result.json())):
            if result.json()[l]["cateName"] == category_name:
                act = "ok"
                category_id = result.json()[l]["id"]
        self.assertEqual(act, "ok")

        # 编辑栏目
        new_now_time = time.strftime("%Y%m%d%H%M%S", time.localtime(time.time()))
        new_category_name = "更新栏目" + new_now_time
        payload = {"id": category_id, "cateName": new_category_name}
        result = self.requests.put("http://182.92.178.83:8081/admin/category/", headers=headers, data=payload)
        print(result.json())  # {'status': 'success', 'msg': '修改成功!'}
        self.assertEqual("修改成功!", result.json()["msg"])

        # 删除栏目
        result = self.requests.delete("http://182.92.178.83:8081/admin/category/" + str(category_id), headers=headers)
        print(result.json())  # {'status': 'success', 'msg': '删除成功!'}
        self.assertEqual("删除成功!", result.json()["msg"])

        # 批量删除
        # 先新建多个栏目
        now_time = time.strftime("%Y%m%d%H%M%S", time.localtime(time.time()))
        category_name_01 = "蔡坨坨栏目" + now_time
        payload = {"cateName": category_name_01}
        headers = {"Cookie": VBlog(self.requests).get_cookie()}
        result = self.requests.post("http://182.92.178.83:8081/admin/category/", headers=headers, data=payload)
        print(result.json())  # {'status': 'success', 'msg': '添加成功!'}
        # 查询所有栏目，取栏目id
        result = self.requests.get("http://182.92.178.83:8081/admin/category/all", headers=headers)
        for l in range(0, len(result.json())):
            if result.json()[l]["cateName"] == category_name_01:
                category_id_01 = result.json()[l]["id"]

        # 先新建多个栏目
        now_time = time.strftime("%Y%m%d%H%M%S", time.localtime(time.time()))
        category_name_02 = "蔡坨坨栏目" + now_time
        payload = {"cateName": category_name_02}
        headers = {"Cookie": VBlog(self.requests).get_cookie()}
        result = self.requests.post("http://182.92.178.83:8081/admin/category/", headers=headers, data=payload)
        print(result.json())  # {'status': 'success', 'msg': '添加成功!'}
        # 查询所有栏目，取栏目id
        result = self.requests.get("http://182.92.178.83:8081/admin/category/all", headers=headers)
        for l in range(0, len(result.json())):
            if result.json()[l]["cateName"] == category_name_02:
                category_id_02 = result.json()[l]["id"]

        result = self.requests.delete(
            "http://182.92.178.83:8081/admin/category/" + str(category_id_01) + "," + str(category_id_02),
            headers=headers)
        print(result.json())  # {'status': 'success', 'msg': '删除成功!'}
        self.assertEqual("删除成功!", result.json()["msg"])

    def test_011_batch_delete_category(self):
        """V部落_批量删除栏目"""
        now_time = time.strftime("%Y%m%d%H%M%S", time.localtime(time.time()))
        category_name = "蔡坨坨栏目" + now_time
        payload = {"cateName": category_name}
        headers = {"Cookie": VBlog(self.requests).get_cookie()}
        result = self.requests.post("http://182.92.178.83:8081/admin/category/", headers=headers, data=payload)
        print(result.json())  # {'status': 'success', 'msg': '添加成功!'}
        self.assertEqual("添加成功!", result.json()["msg"])

        # 查询所有栏目
        result = self.requests.get("http://182.92.178.83:8081/admin/category/all", headers=headers)
        act = 666
        # 查询到刚新增的栏目的栏目名，说明查询成功
        for l in range(0, len(result.json())):
            if result.json()[l]["cateName"] == category_name:
                act = "ok"
                category_id = result.json()[l]["id"]
        self.assertEqual(act, "ok")

        # 编辑栏目
        new_now_time = time.strftime("%Y%m%d%H%M%S", time.localtime(time.time()))
        new_category_name = "更新栏目" + new_now_time
        payload = {"id": category_id, "cateName": new_category_name}
        result = self.requests.put("http://182.92.178.83:8081/admin/category/", headers=headers, data=payload)
        print(result.json())  # {'status': 'success', 'msg': '修改成功!'}
        self.assertEqual("修改成功!", result.json()["msg"])

        # 删除栏目
        result = self.requests.delete("http://182.92.178.83:8081/admin/category/" + str(category_id), headers=headers)
        print(result.json())  # {'status': 'success', 'msg': '删除成功!'}
        self.assertEqual("删除成功!", result.json()["msg"])

        # 批量删除
        # 先新建多个栏目
        now_time = time.strftime("%Y%m%d%H%M%S", time.localtime(time.time()))
        category_name_01 = "蔡坨坨栏目" + now_time
        payload = {"cateName": category_name_01}
        headers = {"Cookie": VBlog(self.requests).get_cookie()}
        result = self.requests.post("http://182.92.178.83:8081/admin/category/", headers=headers, data=payload)
        print(result.json())  # {'status': 'success', 'msg': '添加成功!'}
        # 查询所有栏目，取栏目id
        result = self.requests.get("http://182.92.178.83:8081/admin/category/all", headers=headers)
        for l in range(0, len(result.json())):
            if result.json()[l]["cateName"] == category_name_01:
                category_id_01 = result.json()[l]["id"]

        # 先新建多个栏目
        now_time = time.strftime("%Y%m%d%H%M%S", time.localtime(time.time()))
        category_name_02 = "蔡坨坨栏目" + now_time
        payload = {"cateName": category_name_02}
        headers = {"Cookie": VBlog(self.requests).get_cookie()}
        result = self.requests.post("http://182.92.178.83:8081/admin/category/", headers=headers, data=payload)
        print(result.json())  # {'status': 'success', 'msg': '添加成功!'}
        # 查询所有栏目，取栏目id
        result = self.requests.get("http://182.92.178.83:8081/admin/category/all", headers=headers)
        for l in range(0, len(result.json())):
            if result.json()[l]["cateName"] == category_name_02:
                category_id_02 = result.json()[l]["id"]

        result = self.requests.delete(
            "http://182.92.178.83:8081/admin/category/" + str(category_id_01) + "," + str(category_id_02),
            headers=headers)
        print(result.json())  # {'status': 'success', 'msg': '删除成功!'}
        self.assertEqual("删除成功!", result.json()["msg"])


if __name__ == '__main__':
    unittest.main()
