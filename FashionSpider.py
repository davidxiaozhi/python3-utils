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


    def backWindow(self, window_num=0):
        """
        跳转到制定窗口,并把鼠标移到导航上
        :param window_num: 
        :return: 
        """
        driver = self.spider.browser
        #默认跳转到第一个窗口
        window = driver.window_handles[window_num]
        try:
            driver.switch_to_window(window)
            action_chains = ActionChains(driver)
            nav = driver.find_elements_by_css_selector("div.nav")
            action_chains.move_to_element(nav[0]).perform()
        except Exception as e:
            print(e)
            pass
        return window

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


    def crawOnePage(self):
        time.sleep(3)
        driver = self.spider.browser
        li_all = driver.find_elements_by_css_selector("ul.zw-itemUl.clearfix>li")
        dataList=[]
        for index_li, li in enumerate(li_all):
            try:
                img = li.find_elements_by_css_selector("div.zw-imgBox img")
                self.moveMouseToElement(dim_element=img[0], dim_time=0)
                img_src = img[0].get_attribute("src")
                #print(img_src, end=" ")
                self.saveImg(img_url=img_src)
                imgPaths = img_src.split("/")

                tags = li.find_elements_by_css_selector("div.zw-links.clearfix a")
                tagsList = []
                for index_a, value_a in enumerate(tags):
                    href = value_a.get_attribute("href")
                    text = value_a.text;
                    tagsList.append(text)
                    #print(text, end=",")
                tag_data = "{}.{}   {}".format(imgPaths[-2], imgPaths[-1], ",".join(tagsList))
                #print(tag_data)
                dataList.append(tag_data)
                #print("\n")
            except Exception as e:
                print(e)
                pass
        return dataList

    def crawAllPage(self, t_id):
        #默认第一页打开先读取第一页
        tagList = self.crawOnePage()
        file_name = "{}-{}".format(t_id,1)
        self.saveTextList(file_name,tagList)
        driver = self.spider.browser
        action_chains = ActionChains(driver)
        nextPage = driver.find_elements_by_css_selector("a.J_Ajax.next")
        span = driver.find_elements_by_css_selector("span.next.next-disabled")
        while(len(nextPage)==1 and len(span) == 0):
            page_id = nextPage[0].get_attribute("data-value")
            print("开始第{}页".format(nextPage[0].get_attribute("data-value")))
            action_chains.click(nextPage[0]).perform()
            time.sleep(2)
            tagList =self.crawOnePage()
            file_name = "{}-{}".format(t_id,page_id)
            print(file_name)
            self.saveTextList(file_name,tagList)
            nextPage = driver.find_elements_by_css_selector("a.J_Ajax.next")
            span = driver.find_elements_by_css_selector("span.next.next-disabled")
            action_chains = ActionChains(driver)
            self.moveMouseToElement(nextPage[0])
        # a.J_Ajax.next
        # data-value
        # span.next.next-disabled


    def crawTheTagOfImage(self, tid):
        driver = self.spider.browser
        open_url = "https://guang.taobao.com/ifashion/kan_list_page.htm?spm=a21ct.7779888.0.0.6e21ad92KhEMCx#!gender=2&page={}&tags={}"
        t_url = open_url.format(1, tid)
        # action_chains.move_to_element(value2).pause(3).click(value2).perform()
        js = "window.open('{}')".format(t_url)
        driver.execute_script(js)
        time.sleep(3)
        self.backWindow(-1)
        self.crawAllPage(tid)


    def openNewPage(self, url):
        driver = self.spider.browser
        driver.get(url)
        time.sleep(2)
        #leftlabel = driver.find_elements_by_css_selector(".propertylist-inner.J_ScrollFloat")
        leftlabel = driver.find_elements_by_css_selector(".propertylist-item.J_PropertyList")
        for index, value in enumerate(leftlabel):
            #跳转到第一个窗口,第一个是父窗口 执行操作
            self.backWindow()
            nav = driver.find_elements_by_css_selector("div.nav")
            label_levl_1_title = value.find_elements_by_css_selector(".item-hd")
            label_levl_1_2 = value.find_elements_by_css_selector("ul>li.J_Ajax")
            self.moveMouseToElement(element=nav[0], dim_element=label_levl_1_title[0], dim_time=3)
            print("开始抓取 label-{}-({})".format(label_levl_1_title[0].text, index))
            for index2, value2 in enumerate(label_levl_1_2):
                self.moveMouseToElement(dim_element=value2)
                print("开始抓取 label-index:{}-text:{}-index2:{}-text2:{}".format(index, label_levl_1_title[0].text,
                                                                              index2, value2.text))

                data_value = value2.get_attribute("data-value")
                #爬去图片标签 和 链接
                self.crawTheTagOfImage(data_value)
                driver.close()
                self.backWindow()
                time.sleep(3)
            time.sleep(10)
            self.backWindow()



def main():
    curdir = os.path.dirname(os.path.realpath(__file__))
    binary_location = "/export/App/Google Chrome.app/Contents/MacOS/Google Chrome"
    WINDOW_SIZE = "1920,1080"
    DRIVER_PAHT = os.path.join(curdir, "mac")
    DRIVER_PAHT = os.path.join(DRIVER_PAHT, "data")
    executable_path = os.path.join(DRIVER_PAHT, 'chromedriver')
    spider = FashionSpider(1, driver_path=executable_path, binary_location=binary_location, isBack=True)
    task = FsTask(spider)

    url = "https://guang.taobao.com/ifashion/kan_list_page.htm?spm=a21ct.7779888.0.0.6e21ad92KhEMCx#!gender=2"
    task.openNewPage(url=url)

if __name__ == '__main__':
    main()

