import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from exceptions.product import ProductUnavailable


# LOCATION_ENTERED = False
# 400058

def get_product_information(driver: webdriver.Chrome, product_link: str) -> dict[str, str]:
    # global LOCATION_ENTERED

    # if not LOCATION_ENTERED:
    #     try:
    #         WebDriverWait(driver, 5).until(
    #             EC.element_to_be_clickable(
    #                 (By.CSS_SELECTOR, '.LocationBar__EtaContainer-sc-x8ezho-7')
    #             )
    #         ).click()
    #         WebDriverWait(driver, 5).until(
    #             EC.presence_of_element_located(
    #                 (By.CSS_SELECTOR, "input[placeholder='search delivery location']")
    #             )
    #         ).send_keys('400058')
    #         WebDriverWait(driver, 30).until(
    #             EC.presence_of_all_elements_located(
    #                 (By.CSS_SELECTOR, '.LocationSearchList__LocationListContainer-sc-93rfr7-0')
    #             )
    #         )[0].click()
    #         LOCATION_ENTERED = True
    #         time.sleep(5)
    #     except Exception:
    #         pass
        
    try:
        driver.get(product_link)
    except Exception:
        raise ProductUnavailable(product_link)

    try:
        price_info = driver.find_element(By.CSS_SELECTOR, '.ProductVariants__PriceContainer-sc-1unev4j-7')
    except Exception:
        raise ProductUnavailable(product_link)
    
    try:
        mrp = int(price_info.find_element(By.TAG_NAME, 'span').get_attribute('innerText').lower().split('mrp')[-1].split('₹')[-1].replace(',', '').strip())
        sp = int(price_info.get_attribute('innerText').lower().split('mrp')[0].split('₹')[-1].replace(',', '').strip())
    except ValueError:
        mrp = 'NA'
        sp = 'NA'

    return {
        'mrp': mrp,
        'sp': sp
    }