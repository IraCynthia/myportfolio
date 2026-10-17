import os
import time
import logging
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# 1. Gukora ububiko bwa logs niba budahari
os.makedirs("logs", exist_ok=True)

# 2. Gutunganya uburyo bwa logging
log_filename = datetime.now().strftime("logs/test_run_%Y%m%d_%H%M%S.log")

for handler in logging.root.handlers[:]:
    logging.root.removeHandler(handler)

logging.basicConfig(
    filename=log_filename,
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-5s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

console = logging.StreamHandler()
console.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s | %(levelname)-5s | %(message)s", "%Y-%m-%d %H:%M:%S")
console.setFormatter(formatter)
logging.getLogger("").addHandler(console)

# Hindura hano ushyire link ya GitHub Pages ya portfolio yawe
portfolio_url = "https://iracynthia.github.io/" 
options = webdriver.ChromeOptions()

driver = webdriver.Chrome(options=options)
browser_version = driver.capabilities.get('browserVersion', 'Unknown')

run_start_time = time.time()
logging.info(f"RUN START | portfolio: {portfolio_url} | browser: Chrome {browser_version}")

passed_tests = 0
failed_tests = 0
total_tests = 0

def run_test(test_id, test_desc, action_func, expected_desc):
    global passed_tests, failed_tests, total_tests
    total_tests += 1
    start_time = time.time()
    
    try:
        action_func()
        actual_result = expected_desc
        logging.info(f"{test_id} | {test_desc} | expected: {expected_desc} | actual: {actual_result} | PASS | {time.time() - start_time:.1f} s")
        passed_tests += 1
    except Exception as e:
        failed_tests += 1
        duration = time.time() - start_time
        error_msg = str(e).split('\n')[0]
        actual_result = f"element not found / error"
        
        screenshot_name = f"logs/{test_id}_fail.png"
        driver.save_screenshot(screenshot_name)
        
        logging.error(f"{test_id} | {test_desc} | expected: {expected_desc} | actual: {actual_result} | FAIL | {duration:.1f} s | error: {error_msg} | screenshot: {screenshot_name}")

try:
    # TC-01: Home Page Load
    def test_1():
        driver.get(portfolio_url)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
    run_test("TC-01", "Open Home Page", test_1, "Page loaded successfully")

    # TC-02: Click About Menu
    def test_2():
        about_link = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'About') or contains(@href, 'about')]"))
        )
        about_link.click()
    run_test("TC-02", "Click 'About' Link", test_2, "About section accessible")

    # TC-03: Click Resume Menu
    def test_3():
        resume_link = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'Resume') or contains(@href, 'resume')]"))
        )
        resume_link.click()
    run_test("TC-03", "Click 'Resume' Link", test_3, "Resume section/URL reached")

    # TC-04: Click Projects
    def test_4():
        projects_link = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'Projects') or contains(@href, 'project')]"))
        )
        projects_link.click()
    run_test("TC-04", "Click 'Projects' Link", test_4, "Projects section displayed")

    # TC-05: External Link
    def test_5():
        ext_link = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//a[contains(@href, 'github.com') or contains(@href, 'linkedin.com')]"))
        )
        ext_link.click()
    run_test("TC-05", "Click External Link", test_5, "External link opened")

    # TC-06: Negative Test (Gushaka element itabaho kugira ngo turebe niba log yandika Error na Screenshot)
    def test_6():
        missing_elem = WebDriverWait(driver, 3).until(
            EC.presence_of_element_located((By.ID, "non-existent-section-id"))
        )
        missing_elem.click()
    run_test("TC-06", "Click Missing Section (Negative Test)", test_6, "Element should be found")

finally:
    driver.quit()
    total_duration = time.time() - run_start_time
    logging.info(f"RUN END | total: {total_tests} | passed: {passed_tests} | failed: {failed_tests} | duration: {total_duration:.1f} s")