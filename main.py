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

items_hrefs = ['https://cnsbrand.ru/catalog/diana_micro/sumka_diana_micro_ivory/', 'https://cnsbrand.ru/catalog/diana_micro/sumka_diana_micro_lipstick/', 'https://cnsbrand.ru/catalog/diana_micro/sumka_diana_micro_coal/', 'https://cnsbrand.ru/catalog/diana_micro/sumka_diana_micro_star_crystal/', 'https://cnsbrand.ru/catalog/diana_micro/sumka_diana_micro_kaleido_1/', 'https://cnsbrand.ru/catalog/diana_micro/sumka_diana_micro_kaleido_3/', 'https://cnsbrand.ru/catalog/diana_micro/sumka_diana_micro_kaleido_6/', 'https://cnsbrand.ru/catalog/diana_micro/sumka_diana_micro_kaleido_4/', 'https://cnsbrand.ru/catalog/une_femme_mini/sumka_une_femme_mini_canvas_sandy_siena/', 'https://cnsbrand.ru/catalog/une_femme_mini/sumka_une_femme_mini_canvas_olive_siena/', 'https://cnsbrand.ru/catalog/une_femme_mini/sumka_une_femme_mini_hazelnut/', 'https://cnsbrand.ru/catalog/une_femme_mini/sumka_une_femme_mini_lipstick/', 'https://cnsbrand.ru/catalog/une_femme_mini/sumka_une_femme_mini_coal/', 'https://cnsbrand.ru/catalog/une_femme_mini/sumka_une_femme_mini_siena/', 'https://cnsbrand.ru/catalog/une_femme_mini/sumka_une_femme_mini_olive/', 'https://cnsbrand.ru/catalog/une_femme_mini/sumka_une_femme_mini_caviar/', 'https://cnsbrand.ru/catalog/une_femme_mini/sumka_une_femme_mini_cranberry/', 'https://cnsbrand.ru/catalog/une_femme_mini/sumka_une_femme_mini_dark_chocolate/', 'https://cnsbrand.ru/catalog/une_femme_mini/sumka_une_femme_mini_bubblegum/', 'https://cnsbrand.ru/catalog/une_femme_mini/sumka_une_femme_mini_vanilla/', 'https://cnsbrand.ru/catalog/une_femme_mini/sumka_une_femme_mini_purple/', 'https://cnsbrand.ru/catalog/une_femme_mini/sumka_une_femme_mini_blaze_orange/', 'https://cnsbrand.ru/catalog/une_femme_mini/sumka_une_femme_mini_martini_olive/', 'https://cnsbrand.ru/catalog/delorean_mini_/sumka_delorean_mini_canvas_sandy_siena/', 'https://cnsbrand.ru/catalog/delorean_mini_/sumka_delorean_mini_canvas_olive_siena/', 'https://cnsbrand.ru/catalog/delorean_mini_/sumka_delorean_mini_ash/', 'https://cnsbrand.ru/catalog/delorean_mini_/sumka_delorean_mini_hazelnut/', 'https://cnsbrand.ru/catalog/delorean_mini_/sumka_delorean_mini_sandstone/', 'https://cnsbrand.ru/catalog/delorean_mini_/sumka_delorean_mini_caviar/', 'https://cnsbrand.ru/catalog/delorean_mini_/sumka_delorean_mini_vanilla/', 'https://cnsbrand.ru/catalog/delorean_mini_/sumka_delorean_mini_lime/', 'https://cnsbrand.ru/catalog/delorean_mini_/sumka_delorean_mini_candy/', 'https://cnsbrand.ru/catalog/delorean_mini_/sumka_delorean_mini_purple/', 'https://cnsbrand.ru/catalog/delorean_mini_/sumka_delorean_mini_dark_chocolate/', 'https://cnsbrand.ru/catalog/delorean_mini_/sumka_delorean_mini_cranberry/', 'https://cnsbrand.ru/catalog/delorean_mini_/sumka_delorean_mini_wood/', 'https://cnsbrand.ru/catalog/sumki_cherez_plecho/sumka_bianca_mini_canvas_olive_siena/', 'https://cnsbrand.ru/catalog/sumki_cherez_plecho/sumka_bianca_mini_canvas_sandy_siena/', 'https://cnsbrand.ru/catalog/sumki_cherez_plecho/sumka_bianca_mini_ash/', 'https://cnsbrand.ru/catalog/sumki_cherez_plecho/sumka_bianca_mini_hazelnut/', 'https://cnsbrand.ru/catalog/sumki_cherez_plecho/sumka_bianca_mini_caviar/', 'https://cnsbrand.ru/catalog/mini_sumki_i_klatchi/sumka_bianca_mini_vanilla/', 'https://cnsbrand.ru/catalog/sumki_cherez_plecho/sumka_bianca_mini_sugar_apple/', 'https://cnsbrand.ru/catalog/sumki_cherez_plecho/sumka_bianca_mini_cranberry/', 'https://cnsbrand.ru/catalog/bianca_micro/sumka_bianca_micro_caviar/', 'https://cnsbrand.ru/catalog/paulina/sumka_paulina_caviar/', 'https://cnsbrand.ru/catalog/paulina/sumka_paulina_vanilla/', 'https://cnsbrand.ru/catalog/paulina/sumka_paulina_bubblegum/', 'https://cnsbrand.ru/catalog/diana/sumka_diana_caviar/', 'https://cnsbrand.ru/catalog/diana/sumka_diana_kaleidoscope_pink_mist/', 'https://cnsbrand.ru/catalog/mini_sumki_i_klatchi/sumka_jemma_star_crystal/', 'https://cnsbrand.ru/catalog/sumki_s_ruchkoy/sumka_chantal_sandstone/', 'https://cnsbrand.ru/catalog/sumki_s_ruchkoy/sumka_chantal_caviar/', 'https://cnsbrand.ru/catalog/sumki_s_ruchkoy/sumka_chantal_dark_chocolate/', 'https://cnsbrand.ru/catalog/sumki_s_ruchkoy/sumka_chantal_hazelnut/', 'https://cnsbrand.ru/catalog/evelyne_1/sumka_evelyne_vanilla/', 'https://cnsbrand.ru/catalog/evelyne_1/sumka_evelyne_caviar/', 'https://cnsbrand.ru/catalog/sumki_cherez_plecho/sumka_clare_bubblegum/', 'https://cnsbrand.ru/catalog/sumki_cherez_plecho/sumka_clare_caviar/', 'https://cnsbrand.ru/catalog/sumki_cherez_plecho/sumka_clare_candy/', 'https://cnsbrand.ru/catalog/sumki_na_plecho/sumka_bobbi_mini_dark_chocolate/', 'https://cnsbrand.ru/catalog/sumki_na_plecho/sumka_bobbi_mini_hazelnut/', 'https://cnsbrand.ru/catalog/sumki_na_plecho/sumka_bobbi_mini_ash/', 'https://cnsbrand.ru/catalog/sumki_na_plecho/sumka_bobbi_mini_castle/', 'https://cnsbrand.ru/catalog/sumki_na_plecho/sumka_bobbi_mini_vanilla/', 'https://cnsbrand.ru/catalog/sumki_cherez_plecho/sumka_alexa_bubblegum_1/', 'https://cnsbrand.ru/catalog/sumki_cherez_plecho/sumka_alexa_ash/', 'https://cnsbrand.ru/catalog/sumki_cherez_plecho/sumka_alexa_castle/', 'https://cnsbrand.ru/catalog/sumki_cherez_plecho/sumka_alexa_caviar/', 'https://cnsbrand.ru/catalog/marino/sumka_marino_castle/', 'https://cnsbrand.ru/catalog/marino/sumka_marino_caviar/', 'https://cnsbrand.ru/catalog/marino/sumka_marino_hazelnut/', 'https://cnsbrand.ru/catalog/marino/sumka_marino_ash/', 'https://cnsbrand.ru/catalog/sumki_cherez_plecho/sumka_adelle_mini_caviar/', 'https://cnsbrand.ru/catalog/sumki_cherez_plecho/sumka_adelle_mini_ash/', 'https://cnsbrand.ru/catalog/sumki_cherez_plecho/sumka_adelle_mini_wood/', 'https://cnsbrand.ru/catalog/sumki_cherez_plecho/sumka_adelle_mini_sandstone/', 'https://cnsbrand.ru/catalog/sumki_cherez_plecho/sumka_adelle_mini_lime/', 'https://cnsbrand.ru/catalog/sumki_cherez_plecho/sumka_adelle_mini_candy/', 'https://cnsbrand.ru/catalog/diana_mini/sumka_diana_mini_caviar/', 'https://cnsbrand.ru/catalog/diana_mini/sumka_diana_mini_martini_olive/', 'https://cnsbrand.ru/catalog/diana_mini/sumka_diana_mini_sandstone/', 'https://cnsbrand.ru/catalog/diana_mini/sumka_diana_mini_wood/', 'https://cnsbrand.ru/catalog/diana_mini/sumka_diana_mini_kaleidos_6/', 'https://cnsbrand.ru/catalog/diana_mini/sumka_diana_mini_green_smoke/', 'https://cnsbrand.ru/catalog/diana_mini/sumka_diana_mini_kaleidos/', 'https://cnsbrand.ru/catalog/sumki_cherez_plecho/sumka_cora_vanilla/', 'https://cnsbrand.ru/catalog/aktivnyy_obraz_zhizni/sumka_poyasnaya_brick_caviar/', 'https://cnsbrand.ru/catalog/sumki_cherez_plecho/ryukzak_alma_sandstone/', 'https://cnsbrand.ru/catalog/sumki_cherez_plecho/ryukzak_alma_caviar/', 'https://cnsbrand.ru/catalog/alma/ryukzak_alma_kaleidoscope_coal/', 'https://cnsbrand.ru/catalog/alma/ryukzak_alma_kaleidoscope_green_matcha/', 'https://cnsbrand.ru/catalog/sharon/sumka_sharon_cranberry/', 'https://cnsbrand.ru/catalog/sharon/sumka_sharon_candy/', 'https://cnsbrand.ru/catalog/sharon/sumka_sharon_sandstone/', 'https://cnsbrand.ru/catalog/sharon/sumka_sharon_lime/', 'https://cnsbrand.ru/catalog/sharon/sumka_sharon_ash/', 'https://cnsbrand.ru/catalog/sharon/sumka_sharon_caviar/', 'https://cnsbrand.ru/catalog/sophie/sumka_sophie_caviar/', 'https://cnsbrand.ru/catalog/sophie/sumka_sophie_vanilla/', 'https://cnsbrand.ru/catalog/sumki_cherez_plecho/sumka_adelle_wood/', 'https://cnsbrand.ru/catalog/sumki_cherez_plecho/sumka_adelle_caviar/', 'https://cnsbrand.ru/catalog/sumki_cherez_plecho/sumka_adelle_coal/', 'https://cnsbrand.ru/catalog/sumki_cherez_plecho/sumka_adelle_green_matcha/', 'https://cnsbrand.ru/catalog/sumki_cherez_plecho/sumka_adelle_cranberry/', 'https://cnsbrand.ru/catalog/sumki_na_plecho/sumka_delorean_caviar/', 'https://cnsbrand.ru/catalog/sumki_na_plecho/sumka_delorean_wood/', 'https://cnsbrand.ru/catalog/sumki_na_plecho/sumka_delorean_sandstone/', 'https://cnsbrand.ru/catalog/sumki_na_plecho/sumka_delorean_vanilla/', 'https://cnsbrand.ru/catalog/sumki_na_plecho/sumka_delorean_ash/', 'https://cnsbrand.ru/catalog/sumki_na_plecho/sumka_delorean_hazelnut/', 'https://cnsbrand.ru/catalog/sumki_na_plecho/sumka_caroll_caviar/', 'https://cnsbrand.ru/catalog/odry/sumka_odry_caviar/', 'https://cnsbrand.ru/catalog/sumki_na_plecho/sumka_bobbi_medium_hazelnut/', 'https://cnsbrand.ru/catalog/sumki_na_plecho/sumka_bobbi_medium_dark_chocolate/', 'https://cnsbrand.ru/catalog/sumki_cherez_plecho/sumka_solar_caviar/', 'https://cnsbrand.ru/catalog/sumki_cherez_plecho/sumka_solar_castle/', 'https://cnsbrand.ru/catalog/sumki_cherez_plecho/sumka_solar_medium_pecan_pie/', 'https://cnsbrand.ru/catalog/sumki_cherez_plecho/sumka_solar_medium_caviar/', 'https://cnsbrand.ru/catalog/valerie/sumka_valerie_caviar/', 'https://cnsbrand.ru/catalog/valerie/sumka_valerie_ash/', 'https://cnsbrand.ru/catalog/mone/ryukzak_mone_coal/', 'https://cnsbrand.ru/catalog/gella/sumka_gella_vanilla/', 'https://cnsbrand.ru/catalog/gella/sumka_gella_caviar/', 'https://cnsbrand.ru/catalog/gella/sumka_gella_purple/', 'https://cnsbrand.ru/catalog/gella/sumka_gella_ash/', 'https://cnsbrand.ru/catalog/tina_/sumka_tina_caviar/', 'https://cnsbrand.ru/catalog/tina_/sumka_tina_sandstone/', 'https://cnsbrand.ru/catalog/tina_/sumka_tina_vanilla/', 'https://cnsbrand.ru/catalog/tina_/sumka_tina_sugar_apple/', 'https://cnsbrand.ru/catalog/tina_/sumka_tina_paradise_green/', 'https://cnsbrand.ru/catalog/tina_/sumka_tina_lime/', 'https://cnsbrand.ru/catalog/tina_/sumka_tina_mojito/', 'https://cnsbrand.ru/catalog/maro/sumka_maro_caviar/', 'https://cnsbrand.ru/catalog/maro/sumka_maro_vanilla/', 'https://cnsbrand.ru/catalog/maro/sumka_maro_castle/', 'https://cnsbrand.ru/catalog/une_femme/sumka_une_femme_canvas_sandy_siena/', 'https://cnsbrand.ru/catalog/une_femme/sumka_une_femme_siena/', 'https://cnsbrand.ru/catalog/une_femme/sumka_une_femme_coal/', 'https://cnsbrand.ru/catalog/multiba/sumka_multiba_caviar/', 'https://cnsbrand.ru/catalog/multiba/sumka_multiba_vanilla/', 'https://cnsbrand.ru/catalog/valli/shoper_tranformer_valli_caviar/', 'https://cnsbrand.ru/catalog/valli/shoper_tranformer_valli_wood/', 'https://cnsbrand.ru/catalog/valli/shoper_tranformer_valli_dark_chocolate/', 'https://cnsbrand.ru/catalog/valli/shoper_tranformer_valli_sandstone/', 'https://cnsbrand.ru/catalog/valli/shoper_tranformer_valli_vanilla/', 'https://cnsbrand.ru/catalog/gilda/sumka_gilda_siena/', 'https://cnsbrand.ru/catalog/gilda/sumka_gilda_olive_siena/', 'https://cnsbrand.ru/catalog/aksessuary/panama_cns_siena/', 'https://cnsbrand.ru/catalog/aksessuary/pled_cns_siena/', 'https://cnsbrand.ru/catalog/gilda/sumka_gilda_siena/', 'https://cnsbrand.ru/catalog/sumki_cherez_plecho/sumka_bianca_mini_canvas_olive_siena/']

def kill_all_processes():
    current_proc = psutil.Process()
    for proc in psutil.process_iter():
        if(("chrome" in proc.name() or "python" in proc.name()) and current_proc.pid != proc.pid):
            proc.kill()

def signal_handler(sig, frame):
    print('Прерывание обработано. Завершение всех процессов.')
    kill_all_processes()
    sys.exit(0)

def run_selenium_test(items_hrefs):
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
            driver.get(random.choice(items_hrefs))

            # Ожидание загрузки страницы товара
            try:
                # Нажатие на кнопку "Добавить в корзину"
                add_to_cart_button = driver.find_element(By.CSS_SELECTOR, '[link="basket-modal"]')
                add_to_cart_button.click()
            except:
                print("Ошибка, связанная с нажатием кнопки 'добавить корзину' НЕ В попапе, id: " + thread_id)
                driver.quit()
                return


            # Ожидание, чтобы товар добавился в корзину
            time.sleep(random.uniform(5, 10))

            # Переход в корзину
            driver.get("https://cnsbrand.ru/cart/")

            # Явное ожидание загрузки страницы корзины
            try:
                WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".basket-items-list-item-container")))
                print("Страница корзины загружена успешно, id: " + thread_id)
            except TimeoutException:
                print("Время ожидания истекло, страница корзины НЕ загружена, id: " + thread_id)
                driver.quit()
                return

        except Exception as error:
            print("Ошибка, id: " + thread_id)

        finally:
            driver.quit()
        

def run_tests_on_process(items_hrefs):
    num_threads = 12  # Maximum number of threads per process
    count_proc = 0
    proc_id = str(round(random.uniform(10000, 100000)))

    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        futures = []
        while True:
            if len(futures) < num_threads:
                future = executor.submit(run_selenium_test, items_hrefs)
                futures.append(future)
                
                count_proc += 1
                print("Процесс : " + proc_id + " : " + str(count_proc))
            else:
                # Remove completed futures from the list
                futures = [f for f in futures if not f.done()]
            
            # Sleep to avoid rapid looping
            time.sleep(random.uniform(1, 5))  # Adjust the sleep duration as needed

if __name__ == "__main__":
    kill_all_processes()
    num_threads = 24  # Максимальное количество процессов

    with ProcessPoolExecutor(max_workers=num_threads) as executor:
        for _ in range(num_threads):
            executor.submit(run_tests_on_process, items_hrefs)
            time.sleep(20) 
