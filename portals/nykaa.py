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
    # my_driver = get_chromedriver_without_proxy()
    global COUNT
    
    try:
        driver.get(product_link)
        time.sleep(0.5)
    except Exception:
        ProductUnavailable(product_link)

    try:
        try:
            mrp = float(driver.find_element(By.CLASS_NAME, 'css-u05rr').find_element(By.TAG_NAME, 'span').get_attribute('innerText').strip().strip('₹').replace(',', ''))
        except Exception:
            mrp = 'NA'
        sp = float(driver.find_element(By.CLASS_NAME, 'css-1jczs19').get_attribute('innerText').strip().strip('₹').replace(',', ''))

        return {
            'mrp': mrp,
            'sp': sp
        }
    
    except Exception:
        raise ProductUnavailable(product_link)
    finally:
        # driver.close()
        pass
