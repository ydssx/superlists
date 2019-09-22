from selenium.webdriver.common.keys import Keys
from .base import FunctionalTest




class ItemValidationTest(FunctionalTest):
    """表单输入有效性测试"""
    def test_cannot_add_empty_list_items(self):
        # 伊迪丝访问首页，不小心提交了一个空待办事项
        # 输入框中没输入内容，她就按下了回车键
        self.browser.get(self.live_server_url)
        self.get_item_input_box().send_keys(Keys.ENTER)

        # 浏览器截获了请求
        # 清单页面不会加载
        self.wait_for(lambda:self.browser.find_element_by_css_selector('#id_text:invalid'))

        # 她输入一些文字，错误消失了
        self.get_item_input_box().send_keys('购买牛奶')
        self.wait_for(lambda:self.browser.find_element_by_css_selector('#id_text:valid'))

        #现在能提交了
        self.get_item_input_box().send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1:购买牛奶')

        # 她有点儿调皮，又提交了一个空待办事项
        self.get_item_input_box().send_keys(Keys.ENTER)

        # 浏览器这次也不会放行
        self.wait_for_row_in_list_table('1:购买牛奶')
        self.wait_for(lambda:self.browser.find_element_by_css_selector('#id_text:invalid'))

        # 输入文字之后就能纠正这个错误
        self.get_item_input_box().send_keys('泡茶')
        self.wait_for(lambda:self.browser.find_element_by_css_selector('#id_text:valid'))
        self.get_item_input_box().send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1:购买牛奶')
        self.wait_for_row_in_list_table('2:泡茶')

    def test_cannot_add_duplicate_items(self):
        """测试不能添加重复事项"""
        #伊迪丝访问首页，新建了一个清单
        self.browser.get(self.live_server_url)
        self.get_item_input_box().send_keys('购买雨靴')
        self.get_item_input_box().send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1:购买雨靴')

        #她一不小心输入了一个重复的待办事项
        self.get_item_input_box().send_keys('购买雨靴')
        self.get_item_input_box().send_keys(Keys.ENTER)

        #她看到一条有帮助的错误消息
        self.wait_for(lambda:self.assertEqual(
            self.browser.find_element_by_css_selector('.has-error'),
            "该事项已存在！"))