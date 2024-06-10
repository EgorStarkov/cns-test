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

def run_selenium_test():
    thread_id = str(round(random.uniform(10000, 100000)))

    # Настройка WebDriver для каждого потока
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    try:
        print("Запуск потока, id: " + thread_id)
        # Переход на сайт
        driver.get("https://cnsbrand.ru")

        # Ожидание полной загрузки страницы
        time.sleep(random.uniform(1, 2))

        # Переход в каталог (например, выбираем первый каталог в меню)
        divider = driver.find_element(By.CSS_SELECTOR, ".btn-menu")
        divider.click()
        time.sleep(random.uniform(1, 2))
        catalog_link = driver.find_element(By.CSS_SELECTOR, "#ul_catalog_menu_XEVOpk > li:nth-child(2) > a:nth-child(1)")
        catalog_link.click()

        # Ожидание загрузки страницы каталога
        time.sleep(random.uniform(1, 3))

        # Выбор товара в каталоге
        product_link = driver.find_element(By.CSS_SELECTOR, "a[href*='/catalog/sumki_cherez_plecho/sumka_bianca_mini_canvas_sandy_siena/']")
        product_link.click()

        # Ожидание загрузки страницы товара
        time.sleep(random.uniform(1, 3))
        try:
            # Нажатие на кнопку "Добавить в корзину"
            add_to_cart_button = driver.find_element(By.XPATH, "/html/body/div[2]/div[1]/div[2]/div[2]/div[5]/a")
            add_to_cart_button.click()
        except:
            print("Ошибка, связанная с нажатием кнопки 'добавить корзину' НЕ В попапе, id: " + thread_id)


        # Ожидание, чтобы товар добавился в корзину
        time.sleep(random.uniform(2, 4))

        # Переход в корзину
        try:
            cart_button = driver.find_element(By.XPATH, "/html/body/div[2]/div[3]/div[2]/div[2]/a")
            cart_button.click()
        except:
            print("Ошибка, связанная с нажатием кнопки 'добавить корзину' В попапе, id: " + thread_id)

        # Явное ожидание загрузки страницы корзины
        try:
            WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".basket-page")))
            print("Страница корзины загружена успешно, id: " + thread_id)
        except TimeoutException:
            print("Время ожидания истекло, страница корзины не загружена, id: " + thread_id)

        time.sleep(random.uniform(1, 3))
    except Exception as error:
        print("Тест провален с неизвестной ошибкой (скорее всего это не из-за корзины), id: " + thread_id, error)

    finally:
        driver.quit()
    return

def run_tests_on_process():
    num_threads = 3  # Максимальное количество потоков на процесс

    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        while True:
            time.sleep(3)
            executor.submit(run_selenium_test)

if __name__ == "__main__":
    num_threads = 5  # Максимальное количество процессов

    with ProcessPoolExecutor(max_workers=num_threads) as executor:
        for _ in range(num_threads):
            executor.submit(run_tests_on_process)
