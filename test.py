import sys
import psutil
from selenium import webdriver
from selenium.webdriver.common.by import By
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import ProcessPoolExecutor
import time
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager
import random
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import signal


def kill_all_processes():
    current_proc = psutil.Process()
    for proc in psutil.process_iter():
        if(("chrome" in proc.name() or "python" in proc.name()) and current_proc.pid != proc.pid):
            proc.kill()

def signal_handler(sig, frame):
    print('Прерывание обработано. Завершение всех процессов.')
    kill_all_processes()
    sys.exit(0)

def run_selenium_test():
    thread_id = str(round(random.uniform(10000, 100000)))

    # Настройка WebDriver для каждого потока
    options = Options()
    #options.add_argument('--headless')
    #options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    with webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options) as driver:
        try:
            print("Запуск потока, id: " + thread_id)
            # Переход на сайт
            driver.get("https://cnsbrand.ru/catalog/")

            # Ожидание загрузки страницы товара
            for i in range(11):
                time.sleep(3)
                print("scroll")

                driver. execute_script("window. scrollBy(0, 2000)")

            # Определите CSS селекторы
            outer_selector = '.catalog-item'
            inner_selector = '.pre-order'

            # Найдите все элементы по внешнему селектору
            elements = driver.find_elements(By.CSS_SELECTOR, outer_selector)

            # Проверьте каждый элемент на наличие внутреннего элемента и выведите href
            hrefs = []

            for element in elements:
                if not element.find_elements(By.CSS_SELECTOR, inner_selector):
                    href = element.get_attribute('href')
                    hrefs.append(href)

            print(hrefs)
    
        finally:
            driver.quit()

run_selenium_test()