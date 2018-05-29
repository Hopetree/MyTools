# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import random
import time


class WJX():
    def __init__(self, url):
        self.url = url
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.wait = WebDriverWait(self.driver, 5)

    def _run(self):
        self.driver.get(self.url)
        try:
            question_tags = self.wait.until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, 'div_question'))
            )
        except TimeoutException:
            print('没有找到选项 ！！！')
        else:
            for each_question_tag in question_tags:
                # 获取单个问题的所有选项
                choice_tags = each_question_tag.find_elements_by_xpath(".//ul/li/a")
                num = len(choice_tags)
                choice_num = random.randint(0, num - 1)
                # 随机选择一个选项并点击
                choice_tag = choice_tags[choice_num]
                choice_tag.click()
                # 每个选项选择之后设置一下随机延迟时间，不要选太快了
                time.sleep(random.random() / 2)
        self.driver.find_element_by_id('submit_button').click()


if __name__ == '__main__':
    url = 'https://www.wjx.cn/jq/24325986.aspx'
    wjx = WJX(url)
    wjx._run()
