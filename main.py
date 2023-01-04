from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from util import *
from candidate import *
from special import getStatusFromArticle
import time
import random
import schedule
from time import gmtime, strftime

search_path = "http://api.bilibili.com/x/web-interface/search/type?search_type=video&order=pubdate&keyword=互动抽奖"

options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
options.add_argument('--user-data-dir=C:\\Users\\hongy\\AppData\\Local\\Google\\Chrome\\User Data')          


def getPrizeRelatedStatus(driver, upid):
    driver.get(f"https://space.bilibili.com/{upid}/dynamic")

    WebDriverWait(driver, 200).until(
        EC.presence_of_element_located((By.CLASS_NAME, "v-img"))
    )

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "bili-dyn-item"))
    )

    status_parents = driver.find_elements(By.CLASS_NAME, "bili-dyn-item")
    up_name = driver.find_element(By.ID, "h-name").text
    print(f"发现{len(status_parents)}条动态")

    for status_parent in status_parents:
        reference = status_parent.find_elements(By.CLASS_NAME, "reference")
        if len(reference) > 0:
            lottery = status_parent.find_elements(By.CLASS_NAME, "lottery")
            if lottery and len(lottery) > 0:
                origin_content = status_parent.find_elements(By.CLASS_NAME, "bili-dyn-content__orig__desc")
                origin_content[0].click()
                inspectReference(driver, 2)            
        else:
            album = status_parent.find_elements(By.CLASS_NAME, "bili-album")
            lottery = status_parent.find_elements(By.CLASS_NAME, "lottery")
            if not lottery or len(lottery) == 0:
                continue
            status_id = album[0].get_attribute('dyn-id')
            status_content = status_parent.find_elements(By.CLASS_NAME, "bili-rich-text__content")[0]
            status_time = status_parent.find_elements(By.CLASS_NAME, "bili-dyn-time")[0]
            if checkRelevance(status_content.text) and checkDateDelta(status_time.text) and checkIfFwded(status_id):
                subscribe(driver)
                forward(status_parent, up_name)
                storeFwdedStatus(status_id)

    print(f"up主{up_name}探查完成，前往下一个up主空间")
    time.sleep(random.random() * 8)


def getCandidates(driver):
    driver.get(search_path)
    ups = search(driver.get_cookies(), ['互动抽奖'])
    print(f"candidates: {','.join(ups)}")
    return ups


def job1():
    print (strftime("%Y-%m-%d %H:%M:%S", gmtime()))
    driver = webdriver.Chrome(options=options)
    upList = getUpListFromFile() + getCandidates(driver) 
    for up in upList: getPrizeRelatedStatus(driver, up)


def job2():
    print (strftime("%Y-%m-%d %H:%M:%S", gmtime()))
    driver = webdriver.Chrome(options=options)
    getStatusFromArticle(driver)


if __name__ == "__main__":
    job1()
    schedule.every(2).hours.do(job1)
    #schedule.every(24).hours.do(job2)

    while True:
        schedule.run_pending()
        time.sleep(1)
        