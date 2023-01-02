from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from util import inspectReference
import time
import random

special_links = ["https://space.bilibili.com/5536630/article"]


def getStatusFromArticle(driver):
    for link in special_links:
        getStatus(driver, link)


def getStatus(driver, link):

    driver.get(link)

    original_window = driver.current_window_handle
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "article-item"))
    )

    article_items = driver.find_elements(By.CLASS_NAME, "article-item")

    if article_items:
        for article_item in article_items[0]:
            article_content = article_item.find_elements(By.CLASS_NAME, "article-con")
            if article_content and len(article_content) > 0:
                article_content[0].click()
                wait = WebDriverWait(driver, 10)
                wait.until(EC.number_of_windows_to_be(2))

                for window_handle in driver.window_handles:
                    if window_handle != original_window:
                        driver.switch_to.window(window_handle)
                        break

                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "article-link"))
                )

                article_links = driver.find_elements(By.CLASS_NAME, "article-link")

                for link in article_links:
                    link.click()
                    time.sleep(random.random() * 5)
                    inspectReference(driver, 3)

                time.sleep(random.random() * 10)
                driver.close()
                driver.switch_to.window(original_window)   
                    
