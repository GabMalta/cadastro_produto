

from apps.data_scraping.utils.selenium_webdriver import create_webdriver, wait_until_element_located, wait_until_elements_located
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import time

nav = create_webdriver()



nav.get('https://www.bling.com.br/')

input('Pressione enter para continuar...')

icons = wait_until_elements_located(nav, By.CLASS_NAME, "form-icon")

for icon in icons:
    
    actions = ActionChains(nav)
    actions.move_to_element(icon).click().perform()
    time.sleep(2)
    
    div = wait_until_element_located(nav, By.ID, "meliSearchCatalogsAccordion205633151")
    classes = div.get_attribute('class')
    
    if not "is-checked" in classes.split():
        
        label = wait_until_element_located(nav, By.CSS_SELECTOR, "label[for=meliCatalogSearchAccordionRadio205633151]")
        actions.move_to_element(label).click().perform()
        time.sleep(2)
    
    wait_until_element_located(nav, By.XPATH, "//button[text()='Salvar vínculo']").click()
    time.sleep(2)