"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from django.utils.html import escape
from lists.models import Item ,List

# TODO: Configure your database in settings.py and sync before running tests.


class HomePageTest(TestCase):
    """主页测试类"""
    def test_uses_home_template(self):
        """测试客户端响应是否匹配home.html"""  
        response = self.client.get('/')
        self.assertTemplateUsed(response,'lists/home.html')


class ListViewTest(TestCase):
    """清单视图测试类"""
    def test_displays_only__items_for_that_list(self):
        """测试只显示属于某个清单的所有事项"""
        correct_list=List.objects.create()
        Item.objects.create(text='itemey 1',list=correct_list)
        Item.objects.create(text='itemey 2',list=correct_list)
        other_list=List.objects.create()
        Item.objects.create(text='other list itemey 1',list=other_list)
        Item.objects.create(text='other list itemey 2',list=other_list)

        response=self.client.get(f'/lists/{correct_list.id}/')

        self.assertContains(response, 'itemey 1')
        self.assertContains(response, 'itemey 2')
        self.assertNotContains(response, 'other list itemey 1')
        self.assertNotContains(response, 'other list itemey 2')

    def test_uses_list_template(self):
        """测试是否使用清单模板"""
        list_=List.objects.create()
        response=self.client.get(f'/lists/{list_.id}/')
        self.assertTemplateUsed(response,'lists/list.html')

    def test_passes_correct_list_to_template(self):
        """测试将正确的清单传入模板"""
        other_list=List.objects.create()
        correct_list=List.objects.create()
        response=self.client.get(f'/lists/{correct_list.id}/')
        self.assertEqual(response.context['list'],correct_list)

    def test_can_save_a_POST_request_to_an_existing_list(self):
        """测试能否将POST请求保存到已存在的清单中"""
        other_list=List.objects.create()
        correct_list=List.objects.create()

        self.client.post(f'/lists/{correct_list.id}/',
                         data={'item_text':'A new item for an exsiting list'})

        self.assertEqual(Item.objects.count(),1)
        new_item=Item.objects.first()
        self.assertEqual(new_item.text,'A new item for an exsiting list')
        self.assertEqual(new_item.list,correct_list)

    def test_POST_redirects_to_list_view(self):
        other_list=List.objects.create()
        correct_list=List.objects.create()

        response=self.client.post(f'/lists/{correct_list.id}/',
                                  data={'item_text':'A new item for an exsiting list'})
        self.assertRedirects(response,f'/lists/{correct_list.id}/')


class NewListTest(TestCase):
    """新建清单测试类"""
    def test_can_save_a_POST_request(self):
        response=self.client.post('/lists/new',data={'item_text':'A new list item'})
        self.assertEqual(Item.objects.count(), 1)
        new_item=Item.objects.first()
        self.assertEqual(new_item.text, 'A new list item')

    def test_redirects_after_POST(self):
        response=self.client.post('/lists/new',data={'item_text':'A new list item'})
        new_list=List.objects.first()
        self.assertRedirects(response,f'/lists/{new_list.id}/')

    def test_validation_errors_are_sent_back_to_home_page_template(self):
        response=self.client.post('/lists/new',data={'item_text':''})
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,'lists/home.html')
        excepted_error=escape("You can't have an empty list item")
        self.assertContains(response,excepted_error)

    def test_invalid_list_items_arent_saved(self):
        self.client.post('/lists/new',data={'item_text':''})
        self.assertEqual(List.objects.count(),0)
        self.assertEqual(Item.objects.count(),0)



