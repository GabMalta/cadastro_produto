from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

def create_webdriver():
    service = Service(ChromeDriverManager().install())
    service.path = r'C:\Users\gabri\.wdm\drivers\chromedriver\win64\127.0.6533.88\chromedriver-win32\chromedriver.exe'
    options = webdriver.ChromeOptions()
    #options.add_argument("--headless=new")
    nav = webdriver.Chrome(service=service, options=options)
    return nav

