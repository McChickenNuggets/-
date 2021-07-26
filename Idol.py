import regex
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
import time

def process_xpath(index):
        Xpath = '/html/body/uni-app/uni-page/uni-page-wrapper/uni-page-body/uni-view/uni-view/uni-scroll-view/div/div/div/uni-view/uni-view[3]/uni-navigator['+str(index)+']'
        return Xpath

def get_url(xpath):
        try:
                submit = WAIT.until(EC.element_to_be_clickable((By.XPATH,xpath)))
                submit.click()
                url = browser.current_url
                return url
        except TimeoutException:
                return get_url(xpath)


def parse_url(url):
        pro_id = regex.sub(r'\D',"",url)
        return pro_id

def get_id(index):
        xpath = process_xpath(index+1)
        url = get_url(xpath)
        pro_id = parse_url(url)
        time.sleep(1)
        return pro_id

def get_idol_recent_pro_ids(idol_name,num_pro):
        url = "https://www.taoba.club/#/pages/idols/list?s="+idol_name
        browser.get(url)
        pro_id_list = []
        for i in range(num_pro):
                pro_id = get_id(i)
                browser.get(url)
                pro_id_list.append(pro_id)
        browser.quit()
        return pro_id_list


if __name__ == '__main__':
        browser = webdriver.Chrome()
        WAIT = WebDriverWait(browser, 10)
        id_list=get_idol_recent_pro_ids("胡晓慧",3)
        print(id_list)