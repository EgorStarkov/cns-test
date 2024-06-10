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
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    with webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options) as driver:
        try:
            print("Запуск потока, id: " + thread_id)
            # Переход на сайт
            driver.get("https://cnsbrand.ru/catalog/mone/ryukzak_mone_coal/")

            # Ожидание загрузки страницы товара
            time.sleep(random.uniform(1, 3))
            try:
                # Нажатие на кнопку "Добавить в корзину"
                add_to_cart_button = driver.find_element(By.XPATH, "/html/body/div[2]/div[1]/div[2]/div[2]/div[5]/a")
                add_to_cart_button.click()
            except:
                print("Ошибка, связанная с нажатием кнопки 'добавить корзину' НЕ В попапе, id: " + thread_id)
                print("Кол-во ошибок связанных с корзиной: " + errors_count)


            # Ожидание, чтобы товар добавился в корзину
            time.sleep(random.uniform(15, 20))

            # Переход в корзину
            driver.get("https://cnsbrand.ru/cart/")

            # Явное ожидание загрузки страницы корзины
            try:
                WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".basket-page")))
                print("Страница корзины загружена успешно, id: " + thread_id)
            except TimeoutException:
                print("Время ожидания истекло, страница корзины НЕ загружена, id: " + thread_id)
                errors_count = errors_count + 1
            
            time.sleep(random.uniform(1, 3))
        except Exception as error:
            print("Тест провален с неизвестной ошибкой (скорее всего это не из-за корзины), id: " + thread_id, error)
            print("Кол-во ошибок связанных с корзиной: " + errors_count)

        finally:
            driver.quit()
        

def run_tests_on_process():
    num_threads = 15  # Maximum number of threads per process
    count_proc = 0
    proc_id = str(round(random.uniform(10000, 100000)))

    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        futures = []
        while True:
            if len(futures) < num_threads:
                future = executor.submit(run_selenium_test)
                futures.append(future)
                
                count_proc += 1
                print("Процесс : " + proc_id + " : " + str(count_proc))
            else:
                # Remove completed futures from the list
                futures = [f for f in futures if not f.done()]
            
            # Sleep to avoid rapid looping
            time.sleep(2)  # Adjust the sleep duration as needed

if __name__ == "__main__":
    kill_all_processes()
    num_threads = 14  # Максимальное количество процессов

    with ProcessPoolExecutor(max_workers=num_threads) as executor:
        for _ in range(num_threads):
            executor.submit(run_tests_on_process)
