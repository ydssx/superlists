from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from .base import FunctionalTest

class NewVisitorTest(FunctionalTest):
    """模拟用户访问应用时的测试类"""
    def test_can_start_a_list_and_retrieve_it_later(self):
        """一个在线待办事项应用的功能测试"""
        #伊迪丝去看了这个应用的首页
        self.browser.get(self.live_server_url)

        #测试网页的标题和头部是否包含"To-Do"
        self.assertIn('To-Do',self.browser.title)
        header_text=self.browser.find_element_by_tag_name('h2').text
        self.assertIn('To-Do', header_text)

        #邀请她输入一个待办事项
        inputbox=self.get_item_input_box()
        self.assertEqual(inputbox.get_attribute('placeholder'), 'Enter a to-do item')

        #她在一个文本框中输入了”购买孔雀羽毛”
        inputbox.send_keys('购买孔雀羽毛')

        #她按回车键后，页面更新了
        #待办事项表格中显示了”1:购买孔雀羽毛“
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1:购买孔雀羽毛')

        # 页面中又显示了一个文本框，可以输入其他的待办事项
        # 她输入了“Use peacock feathers to make a fly”（使用孔雀羽毛做假蝇）
        # 伊迪丝做事很有条理
        inputbox=self.get_item_input_box()
        inputbox.send_keys('使用孔雀羽毛做假蝇')
        inputbox.send_keys(Keys.ENTER)

        # 页面再次更新，她的清单中显示了这两个待办事项
        self.wait_for_row_in_list_table('2:使用孔雀羽毛做假蝇')
        self.wait_for_row_in_list_table('1:购买孔雀羽毛')

        # 伊迪丝想知道这个网站是否会记住她的清单
    def test_multiple_users_can_start_lists_at_different_urls(self):
        #伊迪丝新建了一个待办事项清单
        self.browser.get(self.live_server_url)
        inputbox=self.get_item_input_box()
        inputbox.send_keys('购买孔雀羽毛')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1:购买孔雀羽毛')

        #她注意到清单有一个唯一的URL
        edith_list_url=self.browser.current_url
        self.assertRegex(edith_list_url, '/lists/.+')

        #现在一名叫弗朗西斯的新用户访问了网站

        ##我们使用一个新浏览器会话
        ##确保伊迪丝的信息不会从cookie中泄露出去
        self.browser.quit()
        self.browser=webdriver.Firefox()

        #弗朗西斯访问首页
        #页面中看不到伊迪丝的清单
        self.browser.get(self.live_server_url)
        page_text=self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('购买孔雀羽毛',page_text)
        self.assertNotIn('做假蝇', page_text)

        #弗朗西斯输入一个新待办事项，新建一个清单
        inputbox=self.get_item_input_box()
        inputbox.send_keys('购买牛奶')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1:购买牛奶')

        #弗朗西斯获得了他的唯一URL
        francis_list_url=self.browser.current_url
        self.assertRegex(francis_list_url, '/lists/.+')
        self.assertNotEqual(francis_list_url, edith_list_url)

        #这个界面还是没有伊迪丝的清单
        page_text=self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('购买孔雀羽毛',page_text)
        self.assertIn('购买牛奶', page_text)

