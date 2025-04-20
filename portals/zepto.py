import traceback
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from exceptions.product import ProductUnavailable


def get_product_information(driver: webdriver.Chrome, product_link: str) -> dict[str, str]:

    try:
        driver.get(product_link)
    except Exception:
        return {
            'mrp': 'NA',
            'sp': 'NA'
        }

    try:
        mrp = int(WebDriverWait(driver, 1).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '.line-through.font-bold'))
        ).get_attribute('innerText').split('₹')[-1].replace(',', '').strip())
        
        sp = int(WebDriverWait(driver, 1).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "span[class='text-[32px] font-medium leading-[30px] text-[#262A33]']"))
        ).get_attribute('innerText').split('₹')[-1].replace(',', '').strip())
    except Exception:
        try:
            mrp = int(WebDriverWait(driver, 1).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '.line-through.font-bold'))
            ).get_attribute('innerText').split('₹')[-1].replace(',', '').strip())
            
            sp = int(WebDriverWait(driver, 1).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "span[class='text-[32px] font-medium leading-[30px] text-[#262A33]']"))
            ).get_attribute('innerText').split('₹')[-1].replace(',', '').strip())
        except Exception:
            try:
                sp = int(WebDriverWait(driver, 1).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "span[class='text-[32px] font-medium leading-[30px] text-[#262A33]']"))
                ).get_attribute('innerText').split('₹')[-1].replace(',', '').strip())
                return {
                    'mrp': 'NA',
                    'sp': sp
                }
            except Exception:
                return {
                    'mrp': 'NA',
                    'sp': 'NA'
                }

    return {
        'mrp': mrp,
        'sp': sp
    }