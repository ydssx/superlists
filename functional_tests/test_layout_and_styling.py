from selenium.webdriver.common.keys import Keys
from .base import FunctionalTest

class LayoutAndStylingTest(FunctionalTest):
    """布局和外观测试"""
    def test_layout_and_styling(self):
        #伊迪丝访问首页
        self.browser.get(self.live_server_url)
        self.browser.set_window_size(1024,768)

        #她看到输入框完美的居中显示
        inputbox=self.get_item_input_box()
        self.assertAlmostEqual(inputbox.location['x']+inputbox.size['width']/2,512,delta=10)

        #她新建了一个清单，看到输入框仍然完美的居中显示
        inputbox.send_keys('testing')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1:testing')
        inputbox=self.get_item_input_box()
        self.assertAlmostEqual(inputbox.location['x']+inputbox.size['width']/2,512,delta=10)

   