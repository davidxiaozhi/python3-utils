#!/usr/bin/python
#-*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver import ActionChains

import os
import time
import urllib.request as request

class FashionSpider:
    def __init__(self, engine, driver_path, binary_location = None, isBack = True, window_size = None, ):
        self.engine = engine
        self.binary_location = binary_location
        self.browser = None
        self.time_out = 30
        self.driver_path = driver_path
        self.isBack = isBack
        self.window_size = window_size
        self.chrome_options = webdriver.chrome.options.Options()
        self.init_options()
        self.init_browser()

    def init_options(self):
        if self.binary_location:
            self.chrome_options.binary_location=self.binary_location
        if self.window_size:
            self.chrome_options.add_argument("--window-size={}".format(self.window_size))
        if self.isBack:
            self.chrome_options.add_argument("--headless")


    def init_browser(self):
        print("driver_path:{}".format(self.driver_path))
        self.browser = webdriver.Chrome(executable_path = self.driver_path, chrome_options = self.chrome_options)
        self.browser.set_page_load_timeout(30)
        self.browser.implicitly_wait(2)



    def __del__(self):
        if self.browser is not None:
            try:
                self.browser.quit()
            except:pass


class FsTask:
    def __init__(self, spider, save_path = "/export/temp/fashion"):
        self.spider = spider
        self.save_path = save_path
        print("init FsTask")

    def saveImg(self, img_url):
        save_path = os.path.join(self.save_path, "img")
        if os.path.exists(save_path) == False:
            os.makedirs(save_path)
        if img_url != None:
            # 保存图片数据
            try:
                file_name = img_url.split("/")[-1]
                data = request.urlopen(img_url).read()
                save_path = os.path.join(save_path, file_name)
                f = open(save_path, 'wb')
                f.write(data)
                f.close()
            except Exception as e:
                print(e)
                pass

    def saveTextList(self, file_name, taglist):
        save_path = os.path.join(self.save_path, "text")
        if os.path.exists(save_path) == False:
            os.makedirs(save_path)
        if taglist != None:
            f = open(os.path.join(save_path, file_name), 'w')
            for text in taglist:
                try:
                    f.write(str(text+"\n"))
                except Exception as e:
                    print(e)
                    pass
            try:
                f.close()
            except Exception as e:
                pass

    def moveMouseToElement(self, element = None, element_time = 3, dim_element = None, dim_time = 0.1):
        try:
            driver = self.spider.browser
            action_chains = ActionChains(driver)
            if element:
                action_chains.move_to_element(element).perform()
                time.sleep(element_time)
            # 在移动到指定元素,触发鼠标事件
            if dim_element:
                action_chains.move_to_element(dim_element).perform()
                time.sleep(dim_time)
        except Exception as e:
            print(e)
            pass


    def crawOneType(self, items, context_map, type):
        time.sleep(3)
        driver = self.spider.browser
        dataList=[]
        for index_li, li in enumerate(items):
            try:
                #text = li.text()
                if context_map.get(li.text,"None") == "None":
                    print("{} 第 {} 个,内容为:{}".format(type, index_li, li.text))
                    dataList.append(li.text)
            except Exception as e:
                print(e)
                pass
        return dataList




    def openNewPage(self, url):
        context_map = {}
        driver = self.spider.browser
        driver.get(url)
        time.sleep(10)
        action_chains = ActionChains(driver)
        announceTitle = driver.find_elements_by_css_selector("h4.blocks-item-title")
        action_chains.click(announceTitle[0]).perform()
        time.sleep(2)
        sections = driver.find_elements_by_css_selector("section.section")
        # 0 发币上线 1 最新公告
        type_0 = sections[0].find_elements_by_css_selector("li.article-list-item")
        type_1 = sections[1].find_elements_by_css_selector("li.article-list-item")
        fabiList =self.crawOneType(type_0, context_map, type="发币上线")
        annoucList = self.crawOneType(type_1, context_map, type="最新公告")






def main():
    curdir = os.path.dirname(os.path.realpath(__file__))
    binary_location = "/export/App/Google Chrome.app/Contents/MacOS/Google Chrome"
    WINDOW_SIZE = "1920,1080"
    DRIVER_PAHT = os.path.join(curdir, "data")
    DRIVER_PAHT = os.path.join(DRIVER_PAHT, "mac")
    executable_path = os.path.join(DRIVER_PAHT, 'chromedriver')
    spider = FashionSpider(1, driver_path=executable_path, binary_location=binary_location, isBack=False)
    task = FsTask(spider)

    url = "https://support.binance.com/hc/zh-cn"
    #进入币安网首页
    task.openNewPage(url=url)

if __name__ == '__main__':
    main()

