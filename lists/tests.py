"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

import django
from django.test import TestCase

# TODO: Configure your database in settings.py and sync before running tests.


class HomePageTest(TestCase):
    """主页测试类"""
    def test_uses_home_template(self):
        """测试客户端响应是否匹配home.html"""  
        response = self.client.get('/')
        self.assertTemplateUsed(response,'lists/home.html')
