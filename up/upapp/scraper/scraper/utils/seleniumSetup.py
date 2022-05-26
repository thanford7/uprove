import time

from selenium import webdriver
from selenium.common.exceptions import ElementClickInterceptedException, StaleElementReferenceException, \
    NoSuchElementException, TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

from upapp.utils.logger import getLogger
logger = getLogger()

MISSING_DOM_EL_ERRORS = (
    ElementClickInterceptedException,
    NoSuchElementException,
    StaleElementReferenceException,
    TimeoutException
)

WEBDRIVER_WAIT_SECONDS = 3


def getSelenium(isDebug=False):
    chromeOptions = Options()
    if not isDebug:
        logger.info('Setting up Selenium')
        chromeOptions.add_argument('--headless')
        chromeOptions.add_argument('--no-sandbox')
        chromeOptions.add_argument('--disable-extensions')
        chromeOptions.add_argument('--disable-dev-shm-usage')
        chromeOptions.add_argument('--disable-setuid-sandbox')
        chromeOptions.add_argument('--disable-gpu')
        chromeOptions.add_argument('--remote-debugging-port=9222')
        chromeOptions.add_argument('--screen-size=1200x800')
        chromeOptions.binary_location = '/usr/bin/google-chrome'
    driver = webdriver.Chrome(options=chromeOptions, executable_path='/usr/bin/chromedriver')
    # driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chromeOptions, executable_path='/usr/local/bin/chromedriver')
    return driver


def scroll(driver, timeout):
    scroll_pause_time = timeout

    # Get scroll height
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait to load page
        time.sleep(scroll_pause_time)

        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            # If heights are the same it will exit the function
            break
        last_height = new_height


def retryClick(parentEl, cssSelector, isAllowNotFound=False):
    try:
        el = parentEl.find_element(By.CSS_SELECTOR, cssSelector)
        el.click()
        return el
    except MISSING_DOM_EL_ERRORS:
        try:
            el = parentEl.find_element(By.CSS_SELECTOR, cssSelector)
            el.click()
            return el
        except MISSING_DOM_EL_ERRORS as e:
            if isAllowNotFound:
                return None
            else:
                raise e


def getDomElOrNone(driver, parentEl, cssSelector):
    try:
        return WebDriverWait(driver, WEBDRIVER_WAIT_SECONDS).until(lambda d: parentEl.find_element(By.CSS_SELECTOR, cssSelector))
    except MISSING_DOM_EL_ERRORS:
        return None


def getWebElementHtml(driver, webEl):
    return driver.execute_script("return arguments[0].innerHTML;", webEl)


def getWebElementWait(driver, cssSelector, parentEl=None):
    return WebDriverWait(driver, WEBDRIVER_WAIT_SECONDS)\
        .until(lambda d: (parentEl or d).find_element(By.CSS_SELECTOR, cssSelector))
