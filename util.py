from datetime import date, datetime
import time
import random
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains


fwd_sentences = ["争当分子", "抽我抽我", "抽奖三原则，接下来记不住了", "必中"]

def addCookieFromFile(driver):
    stream = open('cookie.txt', 'r')
    data = stream.read()
    items = data.split(';')
    for item in items:
        name = item.split('=')[0]
        value = item.split('=')[1]
        print(name, value)
        driver.add_cookie({   
            "name": name, 
            "value": value,
            "domain": ".bilibili.com",
            "path": "./"
        })


def getUpListFromFile():
    stream = open('prefered_ups.txt', 'r')
    data = stream.readlines()
    return data


def checkDateDelta(dateString):
    today = date.today()
    year = str(today.year)
    if "投稿" in dateString:
        return False
    elif "前" in dateString:
        return True
    elif len(dateString) == 5:
        statusDateString = year + '-' + dateString
        statusDate = datetime.strptime(statusDateString, '%Y-%m-%d').date()
        days_delta = today - statusDate
        if days_delta.days < 21:
            return True
        return False
    elif len(dateString) == 10:
        statusDate = datetime.strptime(dateString, '%Y-%m-%d').date()
        days_delta = today - statusDate
        if days_delta.days < 21:
            return True
        return False
    elif len(dateString) > 10:
        statusDate = datetime.strptime(dateString, '%Y-%m-%d %H:%M').date()
        days_delta = today - statusDate
        if days_delta.days < 21:
            return True
        return False
    return False


def storeFwdedStatus(status_id):
    stream = open('fwded.txt', 'a')
    stream.write(status_id)
    stream.write('\n')
    stream.close()


def getFwdedStatus():
    stream = open('fwded.txt', 'r')
    ids = stream.readlines()
    ids = [id.strip('\n') for id in ids]
    stream.close()
    return ids


def checkIfFwded(id):
    fwdws_ids = getFwdedStatus()
    return id not in fwdws_ids


def checkIfDrawn(driver):
    first_comment = driver.find_elements(By.CLASS_NAME, "list-item")
    if not first_comment:
        return False
    first_comment_p = first_comment[0].find_elements(By.CLASS_NAME, "text")
    if first_comment_p:
        fc = first_comment_p[0].text
        return "恭喜" in fc
    return False


def checkRelevance(text):
    if "抽奖" in text and "预告" not in text:
        return True
    return False


def forward(status_parent, up_name):
    fwd_btn = status_parent.find_elements(By.CLASS_NAME, "forward")[0]
    fwd_btn.click()
    time.sleep(random.random() * 5 + 5)
    fwd_textarea = status_parent.find_elements(By.CLASS_NAME, "bili-rich-textarea__inner")[0]
    fwd_textarea.send_keys(random.choice(fwd_sentences))
    time.sleep(random.random() * 5 + 5)
    confirm_btn = status_parent.find_elements(By.CLASS_NAME, "bili-dyn-forward-publishing__action__btn")[0]
    confirm_btn.click()
    time.sleep(random.random() * 5 + 5)
    print(f"成功于up主{up_name}处转发一条抽奖动态")


def subscribe(driver):

    if driver.find_elements(By.CLASS_NAME, "h-follow"):
        sub_btn = driver.find_elements(By.CLASS_NAME, "h-follow")[0]
        sub_btn.click()
    elif driver.find_elements(By.CLASS_NAME, "bili-dyn-item__avatar"):
        element_to_hover_over = driver.find_elements(By.CLASS_NAME, "bili-dyn-item__avatar")[0]
        hover = ActionChains(driver).move_to_element(element_to_hover_over)
        hover.perform()
        time.sleep(1)

        if driver.find_elements(By.CLASS_NAME, "bili-user-profile-view__info__button"):
            sub_btn = driver.find_elements(By.CLASS_NAME, "bili-user-profile-view__info__button")[0]
            print(sub_btn.text)
            if sub_btn.text == "关注":
                sub_btn.click()
                time.sleep(2)
            driver.execute_script("window.scrollTo(0, 800)") 
            time.sleep(1)
            driver.execute_script("window.scrollTo(0, 0)") 
            submit = driver.find_elements(By.CLASS_NAME, "comment-submit")[0]
            hover = ActionChains(driver).move_to_element(submit)
            hover.perform()
            time.sleep(1)


def inspectReference(driver, expect_windows_num):

    wait = WebDriverWait(driver, 10)
    wait.until(EC.number_of_windows_to_be(expect_windows_num))
    original_window = driver.current_window_handle

    if len(driver.window_handles) >= expect_windows_num:
        driver.switch_to.window(driver.window_handles[expect_windows_num - 1])

    try:
        wait.until(
            EC.presence_of_element_located((By.CLASS_NAME, "bili-rich-text"))
        )
    except:
        driver.close()
        driver.switch_to.window(original_window)
        return

    up_name = driver.find_elements(By.CLASS_NAME, "bili-dyn-title__text")[0].text
    album = driver.find_elements(By.CLASS_NAME, "bili-album")

    if not album or len(album) == 0:
        driver.close()
        driver.switch_to.window(original_window)
        return

    status_id = album[0].get_attribute('dyn-id')
    status_time = driver.find_elements(By.CLASS_NAME, "bili-dyn-time")[0]
    
    if checkDateDelta(status_time.text) and not checkIfDrawn(driver): 
        subscribe(driver)
        time.sleep(random.random() * 5)

    if not checkIfDrawn(driver) and checkDateDelta(status_time.text) and checkIfFwded(status_id):
        forward(driver, up_name)
        storeFwdedStatus(status_id)

    time.sleep(random.random() * 5)
    driver.close()
    driver.switch_to.window(original_window)   