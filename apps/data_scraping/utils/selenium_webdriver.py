from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager


def create_webdriver():
    service = Service(ChromeDriverManager().install())
    # service = Service(executable_path=r'C:\Users\gabri\.wdm\drivers\chromedriver\win64\130.0.6723.91\chromedriver-win32\chromedriver.exe')

    # service.path = r'C:\Users\gabri\.wdm\drivers\chromedriver\win64\130.0.6723.91\chromedriver-win32\chromedriver.exe'
    options = webdriver.ChromeOptions()
    options.add_experimental_option("excludeSwitches", ["enable-logging"])  # reduz logs
    options.add_argument("--log-level=3")  # 0=ALL, 3=ERROR
    options.add_argument("--disable-logging")
    options.add_argument("--disable-dev-shm-usage")
    # options.add_argument("--headless=new")
    nav = webdriver.Chrome(service=service, options=options)
    # service = Service(GeckoDriverManager().install())
    # options = webdriver.FirefoxOptions()
    # nav = webdriver.Firefox(service=service, options=options)
    return nav


def wait_until_element_located(driver, by, value):
    wait = WebDriverWait(driver, 30)
    element = wait.until(EC.presence_of_element_located((by, value)))
    return element


def wait_until_elements_located(driver, by, value):
    wait = WebDriverWait(driver, 30)
    elements = wait.until(EC.presence_of_all_elements_located((by, value)))
    return elements