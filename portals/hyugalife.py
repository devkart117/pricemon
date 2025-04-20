import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from loguru import logger

from utils.selenium_utils import get_chromedriver_without_proxy

from exceptions.product import ProductUnavailable


def get_product_information(driver:webdriver.Chrome, product_link: str) -> dict[str, str]:
    try:
        driver.get(product_link)
    except Exception:
        ProductUnavailable(product_link)

    try:
        sp = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, "//p[@class='font-bold text-4xl sm:text-6xl tracking-tight text-gray-100']"))
        ).get_attribute('innerText').strip().strip('₹').replace(',', '')
        sp = float(sp)

        mrp_element = driver.find_element(By.TAG_NAME, 'del')
        mrp = mrp_element.get_attribute('innerText').strip().strip('₹').replace(',', '')
        mrp = float(mrp)

        try:
            driver.find_element(By.CLASS_NAME, 'AvailableStatus__out-of-stock___2rv_7')
            return {
                'mrp': 'NA',
                'sp': 'NA'
            }
        except Exception:
            return {
                'mrp': mrp,
                'sp': sp
            }
    
    except Exception:
        raise ProductUnavailable(product_link)
