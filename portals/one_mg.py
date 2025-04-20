from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from loguru import logger

from exceptions.product import ProductUnavailable


def get_product_information(driver: webdriver.Chrome, product_link: str) -> dict[str, str]:
    try:
        driver.get(product_link)
    except Exception:
        ProductUnavailable(product_link)

    try:
        sp = float(driver.find_element(By.CLASS_NAME, 'PriceBoxPlanOption__offer-price___3v9x8').get_attribute('innerText').strip().strip('₹').strip('Inclusive of all taxes').replace(',', ''))
    except:
        try:
            sp = float(driver.find_element(By.CLASS_NAME, 'PriceDetails__discount-div___nb724').get_attribute('innerText').strip().strip('MRP').strip('₹').strip('Inclusive of all taxes').replace(',', ''))
        except Exception:
            raise ProductUnavailable(product_link)

    try:
        mrp = float(driver.find_element(By.CLASS_NAME, 'PriceBoxPlanOption__margin-right-4___2aqFt').get_attribute('innerText').strip().strip('₹').replace(',', ''))
    except Exception:
        try:
            mrp = float(driver.find_element(By.CLASS_NAME, 'DiscountDetails__discount-price___Mdcwo').get_attribute('innerText').strip().strip('₹').replace(',', ''))
        except:
            mrp = 'NA'

    return {
        'mrp': mrp,
        'sp': sp
    }