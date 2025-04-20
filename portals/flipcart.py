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
        sp = float(WebDriverWait(driver, 1).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, '.Nx9bqj.CxhGGd')
            )
        ).get_attribute('innerText').strip().strip('₹').replace(',', ''))
        try:
            mrp = float(driver.find_element(By.CSS_SELECTOR, "div[class='yRaY8j A6+E6v']").get_attribute('innerText').strip().strip('₹').replace(',', ''))
        except Exception: 
            mrp = 'NA'

        seller = driver.find_element(By.ID, 'sellerName').find_element(By.TAG_NAME, 'span').find_element(By.TAG_NAME, 'span').get_attribute('innerText').strip()

        if 'assiduus' not in seller.lower():
            try:
                other_sellers_button = driver.find_element(By.XPATH, "//a[div[text()='See other sellers']]")
                other_sellers_button.click()
                try:
                    WebDriverWait(driver, 1).until(
                        EC.presence_of_element_located(
                            (By.XPATH, "//span[text()='Assiduus Distribution']")
                        )
                    )
                    seller += ' / Assiduus Distribution'
                except Exception:
                    pass
            except Exception:
                pass
            
        return {
            'mrp': mrp,
            'sp': sp,
            'seller': seller
        }
    
    except Exception:
        raise ProductUnavailable(product_link)
