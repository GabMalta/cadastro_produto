from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager


def create_webdriver():
    #service = Service(ChromeDriverManager().install())
    service = Service(executable_path=r'C:\Users\gabri\.wdm\drivers\chromedriver\win64\130.0.6723.91\chromedriver-win32\chromedriver.exe')

    #service.path = r'C:\Users\gabri\.wdm\drivers\chromedriver\win64\130.0.6723.91\chromedriver-win32\chromedriver.exe'
    options = webdriver.ChromeOptions()
    #options.add_argument("--headless=new")
    nav = webdriver.Chrome(service=service, options=options)
    # service = Service(GeckoDriverManager().install())
    # options = webdriver.FirefoxOptions()
    # nav = webdriver.Firefox(service=service, options=options)
    return nav
