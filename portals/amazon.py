import os
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

from exceptions.product import ProductUnavailable
from utils.captcha import solve_text_captcha, report_incorrect

CAPTCHAS_SOLVED = 0


def check_for_reload(driver: webdriver.Chrome) -> None:
    alerts = driver.find_elements(By.CLASS_NAME, 'a-alert')

    for alert in alerts:
        if 'reload' in alert.get_attribute('innerText').lower():
            print('reload')
            driver.refresh()
            check_for_reload(driver)

    return


def check_for_captcha(driver: webdriver.Chrome) -> bool:
    try:
        driver.find_element(By.XPATH, '//h4[text()="Type the characters you see in this image:"]')
        return True
    except:
        return False


def solve_captcha(driver: webdriver.Chrome, logger, current_try: int = 1):
    global CAPTCHAS_SOLVED

    if current_try > 5:
        logger.error('Failed to solve captcha after 5 attempts')
        return

    if not os.path.exists('captchas'):
        os.makedirs('captchas')
    
    captcha_img = driver.find_element(By.CSS_SELECTOR, '.a-row img')
    captcha_path = os.path.join(os.getcwd(), 'captchas', 'captcha.png')
    captcha_img.screenshot(captcha_path)

    code, captcha_id = solve_text_captcha(captcha_path, logger)

    driver.find_element(By.ID, 'captchacharacters').send_keys(code)
    driver.find_element(By.TAG_NAME, 'button').click()

    time.sleep(0.5)

    if check_for_captcha(driver):
        report_incorrect(captcha_id, logger)
        return solve_captcha(driver, logger)
    else:
        logger.info('Captcha solved successfully')
        CAPTCHAS_SOLVED += 1
        return


def get_product_information(driver: webdriver.Chrome, product_link: str, logger) -> dict[str, str]:
    
    try:
        driver.get(product_link)
    except Exception:
        raise ProductUnavailable(product_link)

    if check_for_captcha(driver):
        solve_captcha(driver, logger)

    # check_for_reload(driver)

    try:
        product_div = WebDriverWait(driver, 2).until(
            EC.presence_of_element_located(
                (By.ID, 'ppd')
            )
        )
    except TimeoutException:
        driver.refresh()
        try:
            product_div = WebDriverWait(driver, 2).until(
                EC.presence_of_element_located(
                    (By.ID, 'ppd')
                )
            )
        except TimeoutException:
            raise ProductUnavailable(product_link)
        
    # Extract product information
    try:
        apex_desktop_div = driver.find_element(By.CSS_SELECTOR, '#apex_desktop_newAccordionRow')
    except:
        try:
            apex_desktop_div = driver.find_element(By.CSS_SELECTOR, '#apex_desktop')
        except:
            return{
                'url': product_link,
                'mrp': 'NA',
                'sp': 'NA',
                'seller': seller,
                'deal tag': deal_tag,
                'expiry date': expiry_date
            }
    
    try:
        try:
            price_to_pay = float(WebDriverWait(apex_desktop_div, 1).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '.priceToPay .a-price-whole'))
            ).get_attribute('innerText').replace(',', '').replace('.', '').replace('\n', '').strip().strip('₹'))
        except Exception as e:
            price_to_pay = float(apex_desktop_div.find_element(By.CSS_SELECTOR, '.apexPriceToPay .a-offscreen').get_attribute('innerText').replace(',', '').replace('.', '').replace('\n', '').strip().strip('₹'))
    except Exception:
        driver.refresh()
        try:
            price_to_pay = float(WebDriverWait(apex_desktop_div, 1).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '.priceToPay .a-price-whole'))
            ).get_attribute('innerText').replace(',', '').replace('.', '').replace('\n', '').strip().strip('₹'))
        except Exception as e:
            try:
                price_to_pay = float(apex_desktop_div.find_element(By.CSS_SELECTOR, '.apexPriceToPay .a-offscreen').get_attribute('innerText').replace(',', '').replace('.', '').replace('\n', '').strip().strip('₹'))
            except:
                price_to_pay = None

    try:
        basis_price = float(apex_desktop_div.find_element(By.CSS_SELECTOR, '.basisPrice .a-offscreen').get_attribute('innerText').replace(',', '').replace('.', '').replace('\n', '').strip().strip('₹'))
    except Exception:
        basis_price = None

    basis_price = basis_price if basis_price else 'NA'
    price_to_pay = price_to_pay if price_to_pay else 'NA'

    try:
        driver.find_element(By.CSS_SELECTOR, '#dealBadgeSupportingText')
        deal_tag = 'Yes'
    except Exception:
        deal_tag = 'No'

    try:
        expiry_date = driver.find_element(By.CSS_SELECTOR, '#expiryDate_feature_div').get_attribute('innerText').strip().split(':')[-1].strip()
    except Exception:
        expiry_date = 'NA'

    try:
        seller = driver.find_element(By.CSS_SELECTOR, '#merchantInfoFeature_feature_div a').get_attribute('innerText').strip()
    except Exception:
        seller = 'NA'
    
    return {
        'url': product_link,
        'mrp': basis_price,
        'sp': price_to_pay,
        'seller': seller,
        'deal tag': deal_tag,
        'expiry date': expiry_date
    }
