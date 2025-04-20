#!venv/bin/python3

import pprint
import time
import utils.config as _

from loguru import logger

# from pyvirtualdisplay import Display

from utils.selenium_utils import get_chromedriver_without_proxy, get_chromedriver_without_javascript, get_chromedriver_without_javascript_without_headless
from portals.amazon import get_product_information as get_amazon_product_information, CAPTCHAS_SOLVED
from portals.flipcart import get_product_information as get_flipcart_product_information
from portals.one_mg import get_product_information as get_one_mg_product_information
from portals.nykaa import get_product_information as get_nykaa_product_information
from portals.hyugalife import get_product_information as get_hyugalife_product_information
from utils.sheets import get_amazon_data, get_flipcart_data, get_1mg_data, get_nykaa_data, get_hyugalife_data, compile_data
from utils.mail import send_output_mail, send_error_mail, send_email
from exceptions.product import ProductUnavailable


HOST = 'brd.superproxy.io'
PORT = '22225'
USER = 'brd-customer-hl_8805587a-zone-pricemon_willthiswork'
PASS = '125h0s4vd7nh'


if __name__ == '__main__':
    logger.info('starting script')

    send_email('Notification System <dev@kartikcodes.in>', ['dev.kartikaggarwal117@gmail.com'], 'Pricemon Execute!', 'Pricemon script has started execution!', [])

    amazon_output = []
    flipcart_output = []
    one_mg_output = []
    nykaa_output = []
    hyugalife_output = []

    # Fetch data
    try:
        logger.info('loading data')
        amazon_data = get_amazon_data()
        flipcart_data = get_flipcart_data()
        one_mg_data = get_1mg_data()
        nykaa_data = get_nykaa_data()
        hyugalife_data = get_hyugalife_data()
    except Exception as e:
        logger.error(e)
        send_error_mail('Error while loading data from google sheet')
        exit()

    # driver = get_chromedriver_without_proxy()
    driver = get_chromedriver_without_javascript()

    logger.info('scraping amazon data')
    for index, entry in enumerate(amazon_data):
        try:
            ASIN = entry['ASIN']
            Product = entry['Product']
            source_MRP = float(str(entry['source_MRP']).replace(',', '').strip())
            source_SP = float(str(entry['source_SP']).replace(',', '').strip())
            Url = str(entry['Url'])
            if ('http' not in Url.strip().lower()): 
                logger.warning(f'[{index + 1}/{len(amazon_data)}] skipping amazon product, ASIN: {ASIN}')
                continue
            try:
                scraped = get_amazon_product_information(driver, Url, logger)
                logger.debug(f'[{index + 1}/{len(amazon_data)}] scraped amazon product: {Url}')
            except ProductUnavailable:
                scraped = {'mrp': 'NA', 'sp': 'NA', 'seller': 'NA', 'deal tag': 'NA', 'expiry date': 'NA'}
                logger.error(f'[{index + 1}/{len(amazon_data)}] amazon product not found: {Url}')
            amazon_output.append({
                'ASIN': ASIN,
                'Product': Product,
                'source_MRP': source_MRP,
                'scraped_MRP': scraped['mrp'],
                'source_SP': source_SP,
                'scraped_SP': scraped['sp'],
                'seller': scraped['seller'],
                'deal tag': scraped['deal tag'],
                'expiry date': scraped['expiry date'],
                'Url': Url
            })
        except KeyError:
            logger.error('Amazon data structure has been changed')
            send_error_mail('Amazon sheet data structure has been changed')
            exit()
        except ValueError:
            logger.warning(f'[{index + 1}/{len(amazon_data)}] skipping amazon product, ASIN: {ASIN}')
            continue
        
    logger.info('scraping flipkart data')
    for index, entry in enumerate(flipcart_data):
        try:
            Id = entry['Id']
            SKU = entry['SKU']
            source_MRP = float(entry['source_MRP'])
            source_SP = float(entry['source_SP'])
            Url = str(entry['Url'])
            try:
                scraped = get_flipcart_product_information(driver, Url)
                logger.debug(f'[{index + 1}/{len(flipcart_data)}] scraped flipkart product: {Url}')
            except ProductUnavailable:
                scraped = {'mrp': 'NA', 'sp': 'NA', 'seller': 'NA'}
                logger.error(f'[{index + 1}/{len(flipcart_data)}] flipkart product not found: {Url}')
            flipcart_output.append({
                'Id': Id,
                'SKU': SKU,
                'source_MRP': source_MRP,
                'scraped_MRP': scraped['mrp'],
                'source_SP': source_SP,
                'scraped_SP': scraped['sp'],
                'seller': scraped['seller'],
                'Url': Url
            })
        except KeyError:
            logger.error('Flipkart data structure has been changed')
            send_error_mail('Flipkart sheet data structure has been changed')
            exit()

    logger.info('scraping 1mg data')
    for index, entry in enumerate(one_mg_data):
        try:
            Id = entry['Id']
            SKU = entry['SKU']
            source_MRP = float(entry['source_MRP'])
            source_SP = float(entry['source_SP'])
            Url = str(entry['Url'])
            try:
                scraped = get_one_mg_product_information(driver, Url)
                logger.debug(f'[{index + 1}/{len(one_mg_data)}] scraped 1mg product: {Url}')
            except ProductUnavailable:
                scraped = {'mrp': 'NA', 'sp': 'NA'}
                logger.error(f'[{index + 1}/{len(one_mg_data)}] 1mg product not found: {Url}')
            one_mg_output.append({
                'Id': Id,
                'SKU': SKU,
                'source_MRP': source_MRP,
                'scraped_MRP': scraped['mrp'],
                'source_SP': source_SP,
                'scraped_SP': scraped['sp'],
                'Url': Url
            })
            time.sleep(2)
        except KeyError:
            logger.error('1mg data structure has been changed')
            send_error_mail('1mg sheet data structure has been changed')
            exit()

    logger.info('scraping nykaa data')

    for index, entry in enumerate(nykaa_data):
        try:
            Id = entry['Id']
            SKU = entry['SKU']
            source_MRP = float(entry['source_MRP'])
            source_SP = float(entry['source_SP'])
            Url = str(entry['Url'])
            try:
                scraped = get_nykaa_product_information(driver, Url)
                logger.debug(f'[{index + 1}/{len(nykaa_data)}] scraped nykaa product: {Url}')
            except ProductUnavailable:
                scraped = {'mrp': 'NA', 'sp': 'NA'}
                logger.error(f'[{index + 1}/{len(nykaa_data)}] nykaa product not found: {Url}')
            nykaa_output.append({
                'Id': Id,
                'SKU': SKU,
                'source_MRP': source_MRP,
                'scraped_MRP': scraped['mrp'],
                'source_SP': source_SP,
                'scraped_SP': scraped['sp'],
                'Url': Url
            })
        except KeyError:
            logger.error('Nykaa data structure has been changed')
            send_error_mail('Nykaa sheet data structure has been changed')
            exit()

    driver.quit()

    driver = get_chromedriver_without_proxy()

    logger.info('scraping hyugalife data')
    for index, entry in enumerate(hyugalife_data):
        try:
            Id = entry['Id']
            SKU = entry['SKU']
            source_MRP = float(entry['source_MRP'])
            source_SP = float(entry['source_SP'])
            Url = str(entry['Url'])
            try:
                scraped = get_hyugalife_product_information(driver, Url)
                logger.debug(f'[{index + 1}/{len(hyugalife_data)}] scraped hyugalife product: {Url}')
            except ProductUnavailable:
                scraped = {'mrp': 'NA', 'sp': 'NA'}
                logger.error(f'[{index + 1}/{len(hyugalife_data)}] hyugalife product not found: {Url}')
            hyugalife_output.append({
                'Id': Id,
                'SKU': SKU,
                'source_MRP': source_MRP,
                'scraped_MRP': scraped['mrp'],
                'source_SP': source_SP,
                'scraped_SP': scraped['sp'],
                'Url': Url
            })
        except KeyError:
            logger.error('Hyugalife data structure has been changed')
            send_error_mail('Hyugalife sheet data structure has been changed')
            exit()

    # disp = Display()
    # disp.start()
        
    logger.info('data scraping complete, compiling...')
        
    compile_data(amazon_output, flipcart_output, one_mg_output, nykaa_output, hyugalife_output, [], [])

    logger.info('compilation complete, emailing...')

    send_output_mail()

    driver.quit()

    # disp.stop()
    logger.info(f'Captchas solved: {CAPTCHAS_SOLVED}')
    logger.info('script has run to completion!')
