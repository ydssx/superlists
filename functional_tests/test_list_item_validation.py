from selenium.webdriver.common.keys import Keys
from .base import FunctionalTest




class ItemValidationTest(FunctionalTest):
    """表单输入有效性测试"""
    def test_cannot_add_empty_list_items(self):
        # 伊迪丝访问首页，不小心提交了一个空待办事项
        # 输入框中没输入内容，她就按下了回车键
        self.browser.get(self.live_server_url)
        self.browser.find_element_by_id('id_new_item').send_keys(Keys.ENTER)

        # 首页刷新了，显示一个错误消息
        # 提示待办事项不能为空
        self.wait_for(lambda:self.assertEqual(self.browser.find_element_by_css_selector('.has-error').text,
                         "You can't have an empty list item"))

        # 她输入一些文字，然后再次提交，这次没问题了
        self.browser.find_element_by_id('id_new_item').send_keys('购买牛奶')
        self.browser.find_element_by_id('id_new_item').send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1:购买牛奶')

        # 她有点儿调皮，又提交了一个空待办事项
        self.browser.find_element_by_id('id_new_item').send_keys(Keys.ENTER)

        # 在清单页面她看到了一个类似的错误消息
        self.wait_for(lambda:self.assertEqual(self.browser.find_element_by_css_selector('.has-error').text,
                         "You can't have an empty list item"))

        # 输入文字之后就没问题了
        self.browser.find_element_by_id('id_new_item').send_keys('泡茶')
        self.browser.find_element_by_id('id_new_item').send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1:购买牛奶')
        self.wait_for_row_in_list_table('2:泡茶')

        self.fail('finish this test!')
   