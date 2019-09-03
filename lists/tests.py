"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

import django
from django.test import TestCase
from django.urls import resolve
from django.http import HttpRequest

from lists.views import home_page

# TODO: Configure your database in settings.py and sync before running tests.


class HomePageTest(TestCase):
    """主页测试类"""
    def test_root_url_resolves_to_home_page_view(self):
        """测试根url能否解析home_page视图"""
        found = resolve('/')
        self.assertEqual(found.func, home_page)

    def test_home_page_returns_correct_html(self):
        """测试home_page视图能否返回正确的HTML"""
        request = HttpRequest()  
        response = home_page(request)  
        html = response.content.decode('utf8')  
        self.assertTrue(html.startswith('<html>'))  
        self.assertIn('<title>To-Do lists</title>', html)  
        self.assertTrue(html.endswith('</html>'))  
