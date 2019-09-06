from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from django.test import LiveServerTestCase
import time
import unittest

class NewVisitorTest(LiveServerTestCase):

    def setUp(self):
        self.browser=webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def check_for_row_in_list_table(self,row_text):
        table=self.browser.find_element_by_id('id_list_table')
        rows=table.find_elements_by_tag_name('tr')
        self.assertIn(row_text, [row.text for row in rows])

    def test_can_start_a_list_and_retrieve_it_later(self):
        """一个在线待办事项应用的功能测试"""
        #伊迪丝去看了这个应用的首页
        self.browser.get(self.live_server_url)

        #测试网页的标题和头部是否包含"To-Do"
        self.assertIn('To-Do',self.browser.title)
        header_text=self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)

        #邀请她输入一个待办事项
        inputbox=self.browser.find_element_by_id('id_new_item')
        self.assertEqual(inputbox.get_attribute('placeholder'), 'Enter a to-do item')

        #她在一个文本框中输入了”购买孔雀羽毛”
        inputbox.send_keys('购买孔雀羽毛')

        #她按回车键后，页面更新了
        #待办事项表格中显示了”1:购买孔雀羽毛“
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)
        self.check_for_row_in_list_table('1:购买孔雀羽毛')

        # 页面中又显示了一个文本框，可以输入其他的待办事项
        # 她输入了“Use peacock feathers to make a fly”（使用孔雀羽毛做假蝇）
        # 伊迪丝做事很有条理
        inputbox=self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('使用孔雀羽毛做假蝇')
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)

        # 页面再次更新，她的清单中显示了这两个待办事项
        self.check_for_row_in_list_table('1:购买孔雀羽毛')
        self.check_for_row_in_list_table('2:使用孔雀羽毛做假蝇')

        # 伊迪丝想知道这个网站是否会记住她的清单
        [...]



        self.fail('Finish the test!')