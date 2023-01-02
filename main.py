from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from util import *
from candidate import *
import time
import random
import schedule
from time import gmtime, strftime

search_path = "http://api.bilibili.com/x/web-interface/search/type?search_type=video&order=pubdate&keyword=互动抽奖"
fwd_sentences = ["争当分子", "抽我抽我", "抽奖三原则，接下来记不住了", "必中"]


options = webdriver.ChromeOptions()
options.add_argument('--user-data-dir=/Users/hongyujiang/Library/Application Support/Google/Chrome') 


def checkRelevance(text):
    if "抽奖" in text and "预告" not in text:
        return True
    return False


def subscribe():
    if driver.find_elements(By.CLASS_NAME, "h-follow"):
        sub_btn = driver.find_elements(By.CLASS_NAME, "h-follow")[0]
        sub_btn.click()


def forward(status_parent):
    fwd_btn = status_parent.find_elements(By.CLASS_NAME, "forward")[0]
    fwd_btn.click()
    time.sleep(random.random() * 10)
    fwd_textarea = status_parent.find_elements(By.CLASS_NAME, "bili-rich-textarea__inner")[0]
    fwd_textarea.send_keys(random.choice(fwd_sentences))
    time.sleep(random.random() * 10)
    confirm_btn = status_parent.find_elements(By.CLASS_NAME, "bili-dyn-forward-publishing__action__btn")[0]
    confirm_btn.click()
    time.sleep(random.random() * 10)


def getPrizeRelatedStatus(driver, upid):
    driver.get(f"https://space.bilibili.com/{upid}/dynamic")

    WebDriverWait(driver, 200).until(
        EC.presence_of_element_located((By.CLASS_NAME, "level-content"))
    )

    status_parents = driver.find_elements(By.CLASS_NAME, "bili-dyn-item")
    up_name = driver.find_element(By.ID, "h-name").text
    print(f"发现{len(status_parents)}条动态")

    for status_parent in status_parents:
        reference = status_parent.find_elements(By.CLASS_NAME, "bili-album")
        if len(reference) > 0:
            lottery = status_parent.find_elements(By.CLASS_NAME, "lottery")
            original_window = driver.current_window_handle
            if lottery and len(lottery) > 0:
                subscribe_btn = status_parent.find_elements(By.CLASS_NAME, "dyn-orig-author__following")
                if subscribe_btn and len(subscribe_btn) > 0:
                    if subscribe_btn[0].text == '关注':
                        subscribe_btn[0].click()
                        time.sleep(random.random() * 8)
                origin_content = status_parent.find_elements(By.CLASS_NAME, "bili-dyn-content__orig__desc")
                origin_content[0].click()
                wait = WebDriverWait(driver, 10)
    
                wait.until(EC.number_of_windows_to_be(2))
                for window_handle in driver.window_handles:
                    if window_handle != original_window:
                        driver.switch_to.window(window_handle)
                        break

                wait.until(
                    EC.presence_of_element_located((By.CLASS_NAME, "bili-rich-text"))
                )
                album = driver.find_elements(By.CLASS_NAME, "bili-album")
                if not album or len(album) == 0:
                    continue
                status_id = album[0].get_attribute('dyn-id')
                status_time = driver.find_elements(By.CLASS_NAME, "bili-dyn-time")[0]
                if checkDateDelta(status_time.text) and checkIfFwded(status_id):
                    forward(driver)
                    storeFwdedStatus(status_id)
                    print(f"成功于up主{up_name}处转发一条抽奖动态")
 
                time.sleep(random.random() * 5)
                driver.close()
                driver.switch_to.window(original_window)            
        else:
            album = status_parent.find_elements(By.CLASS_NAME, "bili-album")
            if not album or len(album) == 0:
                continue
            status_id = album[0].get_attribute('dyn-id')
            status_content = status_parent.find_elements(By.CLASS_NAME, "bili-rich-text__content")[0]
            status_time = status_parent.find_elements(By.CLASS_NAME, "bili-dyn-time")[0]
            if checkRelevance(status_content.text) and checkDateDelta(status_time.text) and checkIfFwded(status_id):
                subscribe()
                forward(status_parent)
                storeFwdedStatus(status_id)
                print(f"成功于up主{up_name}处转发一条抽奖动态")

    print(f"up主{up_name}探查完成，前往下一个up主空间")
    time.sleep(random.random() * 8)


def getCandidates(driver):
    driver.get(search_path)
    ups = search(driver.get_cookies(), ['互动抽奖'])
    print(f"candidates: {','.join(ups)}")
    return ups


def job():
    print (strftime("%Y-%m-%d %H:%M:%S", gmtime()))
    driver = webdriver.Chrome(options=options)
    upList = getCandidates(driver)
    for up in upList: getPrizeRelatedStatus(driver, up)


if __name__ == "__main__":
    schedule.every(120).minutes.do(job)

    while True:
        schedule.run_pending()
        time.sleep(1)
        