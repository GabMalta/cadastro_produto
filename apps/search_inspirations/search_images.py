from data_scraping.utils.selenium_webdriver import create_webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time

def search_images(query, num_images=10):
    driver = create_webdriver()
    driver.get('https://www.pinterest.com/')
    
    time.sleep(5)
    driver.find_element(By.XPATH, '//*[@id="__PWS_ROOT__"]/div/div[1]/div/div[1]/div/div[2]/div[2]/button/div/div').click()
    time.sleep(5)
    driver.find_element(By.ID, 'email').send_keys('textil.legitima@gmail.com')
    driver.find_element(By.ID, 'password').send_keys('Gab202127*')
    driver.find_element(By.XPATH, '//*[@id="__PWS_ROOT__"]/div/div[1]/div[2]/div/div/div/div/div/div[4]/form/div[7]/button/div').click()
    
    
    time.sleep(10)
    search_box = driver.find_element(By.NAME, 'searchBoxInput')
    search_box.send_keys(query)
    time.sleep(3)
    search_box.send_keys(Keys.RETURN)
    
    time.sleep(3)
    
    image_urls = []
    images = driver.find_elements(By.CSS_SELECTOR, 'img.hCL.kVc.L4E.MIw')
    for img in images[:num_images]:
        src = img.get_attribute('src')
        if src:
            image_urls.append(src)
    
    driver.quit()
    return image_urls