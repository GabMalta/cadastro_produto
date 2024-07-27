from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

def create_webdriver():
    service = Service(ChromeDriverManager().install())
    options = webdriver.ChromeOptions()
    #options.add_argument("--headless=new")
    nav = webdriver.Chrome(service=service, options=options)
    return nav
