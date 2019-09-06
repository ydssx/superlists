"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

import django
from django.test import TestCase
from lists.models import Item

# TODO: Configure your database in settings.py and sync before running tests.


class HomePageTest(TestCase):
    """主页测试类"""
    def test_uses_home_template(self):
        """测试客户端响应是否匹配home.html"""  
        response = self.client.get('/')
        self.assertTemplateUsed(response,'lists/home.html')

    def test_can_save_a_POST_request(self):
        response=self.client.post('/',data={'item_text':'A new list item'})
        self.assertEqual(Item.objects.count(), 1)
        new_item=Item.objects.first()
        self.assertEqual(new_item.text, 'A new list item')

    def test_redirects_after_POST(self):
        response=self.client.post('/',data={'item_text':'A new list item'})
        self.assertEqual(response.status_code,302)
        self.assertEqual(response['location'],'/')

    def test_only_saves_items_when_necessary(self):
        """测试只在必要时保存待办事项"""
        self.client.get('/')
        self.assertEqual(Item.objects.count(), 0)

    def test_displays_all_list_items(self):
        Item.objects.create(text='itemey 1')
        Item.objects.create(text='itemey 2')


        response=self.client.get('/')

        self.assertIn('itemey 1',response.content.decode())
        self.assertIn('itemey 2',response.content.decode())

class ItemModelTest(TestCase):
    """模型测试类"""
    def test_saving_and_retrieving_items(self):
        first_item=Item()
        first_item.text='The first(ever) list item'
        first_item.save()

        second_item=Item()
        second_item.text='Item the second'
        second_item.save()

        saved_items=Item.objects.all()
        self.assertEqual(saved_items.count(), 2)
        first_saved_item=saved_items[0]
        second_saved_item=saved_items[1]
        self.assertEqual(first_saved_item.text, 'The first(ever) list item')
        self.assertEqual(second_saved_item.text, 'Item the second')

