# Импорт необходимых библиотек
import os  # Импорт библиотеки для работы с операционной системой
import time  # Импорт библиотеки для работы со временем
import requests  # Импорт библиотеки для выполнения HTTP-запросов
import random  # Импорт библиотеки для генерации случайных чисел
from selenium import webdriver  # Импорт библиотеки для автоматизации браузера
from selenium.webdriver.common.by import By  # Импорт класса By для работы с методами поиска элементов
# Определение пути к драйверу Chrome и его настройки
devastor_PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))  # Получение пути к текущему каталогу проекта
devastor_DRIVER_BIN = os.path.join(devastor_PROJECT_ROOT, "./chromedriver")  # Сбор пути к исполняемому файлу драйвера Chrome
devastor_options = webdriver.ChromeOptions()  # Создание объекта с настройками браузера Chrome
devastor_options.add_argument("--disable-dev-shm-usage")  # Добавление аргумента для отключения /dev/shm
devastor_options.add_argument("--no-sandbox")  # Добавление аргумента для отключения песочницы (sandbox)
devastor_options.add_argument('window-size=1920x1480')  # Установка размера окна браузера
devastor_options.page_load_strategy = 'eager'  # Установка стратегии загрузки страницы "eager" (по мере загрузки)
# Создание объекта браузера Chrome
devastor_browser = webdriver.Chrome(options=devastor_options, executable_path=devastor_DRIVER_BIN)  # Инициализация браузера Chrome
devastor_browser.implicitly_wait(0)  # Установка неявного ожидания элементов (0 секунд)
devastor_browser.set_window_position(0, 0, windowHandle='current')  # Установка позиции окна браузера
# Создание сессии для HTTP-запросов
devastor_session = requests.Session()  # Инициализация сессии для выполнения запросов
# Настройка заголовков для HTTP-запросов
devastor_session.headers.update({
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'en-US,en;q=0.9',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
})
# Определение функции для загрузки изображения
def download_image(devastor_image_url, devastor_folder, devastor_filename):
    try:
        response = devastor_session.get(devastor_image_url)  # Отправка HTTP-запроса для загрузки изображения
        if response.status_code == 200:
            devastor_filename = devastor_filename + ".jpg"
            with open(os.path.join(devastor_folder, devastor_filename), 'wb') as f:
                f.write(response.content)  # Запись содержимого ответа в файл
        else:
            print(f"Failed to download {devastor_filename} - Status Code {response.status_code}")
        time.sleep(random.uniform(1, 3))  # Пауза для случайной задержки
    except Exception as e:
        print(f"Error downloading image {devastor_filename}: {str(e)}")
# URL-адрес сайта для сканирования
devastor_url = "https://www.net-a-porter.com/en-gb/shop/clothing"
# Открытие браузера и переход по URL-адресу
devastor_browser.get(devastor_url)
# Инициализация списка для хранения типов одежды
devastor_cloth_types = []
# Поиск контейнера с типами одежды
devastor_cloth_list_container = devastor_browser.find_elements(By.XPATH, "//*[@class='AccordionSection3__contentChildWrapper']")[0]
# Поиск элементов с типами одежды
devastor_cloth_list = devastor_cloth_list_container.find_elements(By.XPATH, "*[@class='Filter52__filterLine']")
# Обход элементов и добавление их в список
for devastor_cloth_type in devastor_cloth_list:
    devastor_cloth_type_short = devastor_cloth_type.get_attribute("href").split('/')[-1]
    if (devastor_cloth_type_short != "clothing"):
        devastor_cloth_types.append(devastor_cloth_type_short)
# Создание основной папки для сохранения данных
devastor_MAIN_FOLDER_NAME = "net-a-porter"
os.makedirs(devastor_MAIN_FOLDER_NAME, exist_ok=True)
# Обход типов одежды
for devastor_cloth_type_s in devastor_cloth_types:
    # Создание подпапки для каждого типа одежды
    devastor_SUB_FOLDER_NAME = os.path.join(devastor_MAIN_FOLDER_NAME, devastor_cloth_type_s)
    os.makedirs(devastor_SUB_FOLDER_NAME, exist_ok=True)
    # Формирование URL-адреса для типа одежды
    devastor_url_part = devastor_url + "/" + devastor_cloth_type_s
    # Переход по URL-адресу
    devastor_browser.get(devastor_url_part)
    # Поиск контейнеров с элементами типа одежды
    devastor_cloth_type_s_containers = devastor_browser.find_elements(By.XPATH, "//*[@class='ProductList52__productItemContainer']")
    # Обход элементов
    for devastor_cloth_type_s_container in devastor_cloth_type_s_containers:
        # Прокрутка элемента в видимую область
        devastor_browser.execute_script("arguments[0].scrollIntoView();", devastor_cloth_type_s_container)
        try:
            # Поиск изображений для каждого элемента
            devastor_cloth_type_s_container_img_both = devastor_cloth_type_s_container.find_element(By.CLASS_NAME, "DoubleImage18").find_elements(By.XPATH, "./child::*")
            devastor_cloth_type_s_container_primary_img = devastor_cloth_type_s_container_img_both[0].find_element(By.TAG_NAME, "img")
            devastor_cloth_type_s_container_primary_img_url = devastor_cloth_type_s_container_primary_img.get_attribute("src")
            devastor_cloth_type_s_container_secondary_img = devastor_cloth_type_s_container_img_both[1].find_element(By.TAG_NAME, "img")
            devastor_cloth_type_s_container_secondary_img_url = devastor_cloth_type_s_container_secondary_img.get_attribute("src")
            # Создание папок для сохранения изображений
            devastor_CLOTH_FOLDER_NAME = os.path.join(devastor_SUB_FOLDER_NAME, "cloth")
            os.makedirs(devastor_CLOTH_FOLDER_NAME, exist_ok=True)
            devastor_PERSON_FOLDER_NAME = os.path.join(devastor_SUB_FOLDER_NAME, "person")
            os.makedirs(devastor_PERSON_FOLDER_NAME, exist_ok=True)
            # Формирование имен файлов из атрибутов элементов
            devastor_cloth_type_s_container_primary_img_filename = devastor_cloth_type_s_container_primary_img.get_attribute("alt").replace(" ", "_")
            devastor_cloth_type_s_container_secondary_img_filename = devastor_cloth_type_s_container_secondary_img.get_attribute("alt").replace(" ", "_")
            # Загрузка изображений
            download_image(devastor_cloth_type_s_container_primary_img_url, devastor_CLOTH_FOLDER_NAME, devastor_cloth_type_s_container_primary_img_filename)
            download_image(devastor_cloth_type_s_container_secondary_img_url, devastor_PERSON_FOLDER_NAME, devastor_cloth_type_s_container_secondary_img_filename + "_person")
        except:
            pass
# Завершение работы браузера
devastor_browser.close()
devastor_browser.quit()



# Функция для динамического ожидания загрузки веб-элемента
def devastor_wait_for_element_to_load(devastor_obj, devastor_xpath, timeout=30):
    start_time = time.time()  # Запись текущего времени начала ожидания
    while time.time() - start_time < timeout:  # Проверка, не истек ли таймаут
        try:
            element = devastor_obj.find_element(By.XPATH, devastor_xpath)  # Попытка найти элемент по XPath
            if element.is_displayed():  # Проверка, отображается ли элемент
                return element  # Если элемент найден и отображается, вернуть его
        except Exception:
            pass  # Если возникла ошибка при поиске элемента, продолжить ожидание
        time.sleep(1)  # Подождать 1 секунду перед следующей попыткой
    raise TimeoutError(f"Timed out waiting for element with xpath: {devastor_xpath}")  # Если истек таймаут, вызвать исключение





