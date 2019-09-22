"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from django.utils.html import escape
from lists.models import Item ,List
from lists.forms import ItemForm
from unittest import skip

# TODO: Configure your database in settings.py and sync before running tests.


class HomePageTest(TestCase):
    """主页测试类"""
    def test_uses_home_template(self):
        """测试客户端响应是否匹配home.html"""  
        response = self.client.get('/')
        self.assertTemplateUsed(response,'lists/home.html')

    def test_home_page_uses_item_form(self):
        """测试主页使用新的表单"""
        response = self.client.get('/')
        self.assertIsInstance(response.context['form'],ItemForm)


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
                         data={'text':'A new item for an exsiting list'})

        self.assertEqual(Item.objects.count(),1)
        new_item=Item.objects.first()
        self.assertEqual(new_item.text,'A new item for an exsiting list')
        self.assertEqual(new_item.list,correct_list)

    def test_POST_redirects_to_list_view(self):
        other_list=List.objects.create()
        correct_list=List.objects.create()

        response=self.client.post(f'/lists/{correct_list.id}/',
                                  data={'text':'A new item for an exsiting list'})
        self.assertRedirects(response,f'/lists/{correct_list.id}/')

    def test_vlidation_errors_end_up_on_lists_page(self):
        list_=List.objects.create()
        response=self.client.post(f'/lists/{list_.id}/',data={'text':''})
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,'lists/list.html')
        excepted_error=escape("表单提交不能为空！")
        self.assertContains(response,excepted_error)

    def test_display_item_form(self):
        list_=List.objects.create()
        response=self.client.get(f'/lists/{list_.id}/')
        self.assertIsInstance(response.context['form'],ItemForm)
        self.assertContains(response,'name="text"')

    def post_invalid_input(self):
        list_=List.objects.create()
        return self.client.post(f'/lists/{list_.id}/',data={'text':''})

    def test_for_invalid_input_nothing_saved_to_db(self):
        self.post_invalid_input()
        self.assertEqual(Item.objects.count(),0)

    def test_for_invalid_input_renders_list_template(self):
        response=self.post_invalid_input()
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,'lists/list.html')

    def test_for_invalid_input_passes_form_to_template(self):
        response=self.post_invalid_input()
        self.assertIsInstance(response.context['form'],ItemForm)

    def test_for_invalid_input_shows_error_on_page(self):
        """测试无效输入在页面显示错误提示"""
        response=self.post_invalid_input()
        excepted_error=escape("表单提交不能为空！")
        self.assertContains(response,excepted_error)

    @skip
    def test_duplicate_item_validation_errors_end_up_on_lists_page(self):
        """测试在清单页面显示输入重复事项错误"""
        list1=List.objects.create()
        item=Item.objects.create(list=list1,text='textey')
        response=self.client.post(f'/lists/{list1.id}/',data={'text':'textey'})

        excepted_error=escape('该事项已存在！')
        self.assertContains(response,excepted_error)
        self.assertTemplateUsed(response,lists/list.html)
        self.assertEqual(Item.objects.all().count(),1)


class NewListTest(TestCase):
    """新建清单测试类"""
    def test_can_save_a_POST_request(self):
        response=self.client.post('/lists/new',data={'text':'A new list item'})
        self.assertEqual(Item.objects.count(), 1)
        new_item=Item.objects.first()
        self.assertEqual(new_item.text, 'A new list item')

    def test_redirects_after_POST(self):
        response=self.client.post('/lists/new',data={'text':'A new list item'})
        new_list=List.objects.first()
        self.assertRedirects(response,f'/lists/{new_list.id}/')

    def test_for_invalid_input_renders_home_template(self):
        response=self.client.post('/lists/new',data={'text':''})
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,'lists/home.html')

    def test_validation_errors_are_shown_on_home_page(self):
        response=self.client.post('/lists/new',data={'text':''})
        excepted_error=escape("表单提交不能为空！")
        self.assertContains(response,excepted_error)

    def test_for_invalid_input_passes_form_to_template(self):
        response=self.client.post('/lists/new',data={'text':''})
        self.assertIsInstance(response.context['form'],ItemForm)

    def test_invalid_list_items_arent_saved(self):
        self.client.post('/lists/new',data={'text':''})
        self.assertEqual(List.objects.count(),0)
        self.assertEqual(Item.objects.count(),0)


