import os
import time
import uuid
from logger import log
import sys
from selenium import webdriver
from PIL import ImageGrab
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

DOWNLOAD_FOLDER = "D:\\Programs\\TLScreen\\TLScreen\\Telegram\\"
MAX_MESSAGES = 1000
EXTENSIONS_DOCUMENT = [".docx", ".txt"]
URL = "https://web.telegram.org/#/im"


def create_firefox_profile():
    fp = webdriver.FirefoxProfile(os.environ["MProfile"])
    fp.set_preference("browser.download.folderList", 2)
    fp.set_preference("browser.download.manager.showWhenStarting", False)
    fp.set_preference("browser.download.dir",
                      "{}TmpDownload".format(DOWNLOAD_FOLDER))
    fp.set_preference("browser.helperApps.alwaysAsk.force", False)
    fp.set_preference('browser.helperApps.neverAsk.saveToDisk',
                      "application/octet-stream")
    return fp


def screen_object_profile(driver):
    chats = wait.until(EC.presence_of_element_located(
        (By.XPATH, "/html/body/div[1]/div[2]/div/div[1]/div[2]/div/div[1]/ul/li[1]")))

    button_menu = wait.until(EC.presence_of_element_located(
        (By.XPATH, "/html/body/div[1]/div[1]/div/div/div[1]/div/a/div")))

    button_menu.click()
    log.info("Переход в меню профиля")

    button_settings = wait.until(EC.presence_of_element_located(
        (By.XPATH, "/html/body/div[1]/div[1]/div/div/div[1]/div/ul/li[3]/a")))

    button_settings.click()
    log.info("Переход в настройки профиля")

    button_active_sessions = wait.until(EC.presence_of_element_located(
        (By.XPATH, "/html/body/div[5]/div[2]/div/div/div[3]/div/div[4]/div[3]/a")))

    if not os.path.isdir(DOWNLOAD_FOLDER):
        os.mkdir(DOWNLOAD_FOLDER)
        log.info(f"Создана папка {DOWNLOAD_FOLDER}")

    img = ImageGrab.grab()
    img.save(DOWNLOAD_FOLDER + 'profile.jpg')
    log.info("Сделан снимок профиля profile.jpg")

    button_active_sessions.click()

    active_sessions = wait.until(EC.presence_of_element_located(
        (By.XPATH, "/html/body/div[6]/div[2]/div/div/div[2]/div/div/div[1]/ul")))
    log.info("Загружены активные сессии профиля")

    img = ImageGrab.grab()
    img.save(DOWNLOAD_FOLDER + 'active_sessions.jpg')
    log.info("Сделан снимок активных сессий пользователя active_sessions.jpg")

    driver.find_element_by_xpath(
        "/html/body/div[6]/div[2]/div/div/div[1]/div[1]/div/a").click()
    driver.find_element_by_xpath(
        "/html/body/div[5]/div[2]/div/div/div[1]/div[1]/div[1]/a[1]").click()


def screen_headers_chats(driver):
    slider = driver.find_element_by_xpath(
        "/html/body/div[1]/div[2]/div/div[1]/div[2]/div/div[2]/div")

    height_chats = driver.find_element_by_xpath(
        "/html/body/div[1]/div[2]/div/div[1]/div[2]/div").size["height"]

    slider_y_position = slider.location["y"]

    img = ImageGrab.grab()
    img.save(DOWNLOAD_FOLDER + "chats_0.jpg")
    log.info("Сделан 0-й снимок заголовков чатов chats_0.jpg")

    count = 1

    while True:
        driver.execute_script(
            "document.getElementsByClassName(\"im_dialogs_scrollable_wrap  nano-content\")[0].scroll({}, {})".format(0, height_chats * count * 0.9))  # 0.9 - 90% от высоты диалога

        if slider_y_position == slider.location["y"]:
            break

        slider_y_position = slider.location["y"]
        time.sleep(0.5)
        img = ImageGrab.grab()
        img.save(DOWNLOAD_FOLDER + "chats_{}.jpg".format(count))
        log.info(
            f"Сделан {count}-й снимок заголовков чатов chats_{count}.jpg")
        count = count + 1

    driver.execute_script(
        "document.getElementsByClassName(\"im_dialogs_scrollable_wrap  nano-content\")[0].scroll({}, {})".format(0, 0))


def screen_chat(driver):
    chat_header = wait.until(EC.presence_of_element_located(
        (By.XPATH, "/html/body/div[1]/div[1]/div/div/div[2]/div/div[2]/a")))
    chat_header.click()

    chat_name = driver.find_element_by_xpath(
        "/html/body/div[5]/div[2]/div/div/div[1]/div[2]/div[2]/div[1]").text

    path_chat_folder = "{}{}".format(DOWNLOAD_FOLDER, chat_name)

    if os.path.isdir(path_chat_folder):
        path_chat_folder = path_chat_folder + "_{}".format(uuid.uuid4())

    path_chat_folder = path_chat_folder + "\\"

    os.mkdir(path_chat_folder)
    log.info("Создана папка path_chat_folder")

    img = ImageGrab.grab()
    img.save(path_chat_folder + "profile.jpg")
    log.info(
        f"Сделан снимок профиля собеседника {path_chat_folder}profile.jpg")

    driver.find_element_by_xpath(
        "/html/body/div[5]/div[2]/div/div/div[1]/div[1]/div[1]/a").click()

    slider_chat = driver.find_element_by_xpath(
        "/html/body/div[1]/div[2]/div/div[2]/div[3]/div/div[2]/div[2]/div")
    slider_chat_y = slider_chat.location["y"]

    hystory_chat = driver.find_element_by_xpath(
        "/html/body/div[1]/div[2]/div/div[2]/div[3]/div/div[2]/div[1]/div")

    hystory_chat_height = hystory_chat.size["height"]

    # scount = 1
    while True:
        driver.execute_script(
            "document.getElementsByClassName(\"im_history_scrollable_wrap\")[0].scroll(0, 0)")
        time.sleep(0.5)
        try:
            progress = WebDriverWait(driver, 40).until(EC.invisibility_of_element_located(
                (By.XPATH, "/html/body/div[1]/div[2]/div/div[2]/div[3]/div/div[2]/div[1]/div/div[1]/div[2]/div[1]")))
        except Exception as except_info:
            break

        num_messages = len(driver.find_elements_by_css_selector(
            "div.im_history_messages_peer:not(.ng-hide) > div.im_history_message_wrap"))

        if (hystory_chat_height == hystory_chat.size["height"]) or (MAX_MESSAGES <= num_messages):
            break

        hystory_chat_height = hystory_chat.size["height"]

    chat_height = driver.find_element_by_xpath(
        "/html/body/div[1]/div[2]/div/div[2]/div[3]/div/div[2]").size["height"]

    img = ImageGrab.grab()
    img.save(path_chat_folder + "chat_0.jpg")
    log.info(f"Сделан 0-й снимок диалога {path_chat_folder}chat_0.jpg")

    screen_number = 1
    while True:
        scroll_height = chat_height * screen_number * 0.9
        driver.execute_script(
            "document.getElementsByClassName(\"im_history_scrollable_wrap\")[0].scroll({}, {})".format(0, scroll_height))
        time.sleep(0.5)
        img = ImageGrab.grab()
        img.save(path_chat_folder + "\\chat_{}.jpg".format(screen_number))
        log.info(f"{path_chat_folder}\chat_{screen_number}.jpg")

        if scroll_height >= hystory_chat.size["height"]:
            break
        screen_number = screen_number + 1

    log.info("Начало загрузки вложений")
    audios = driver.find_elements_by_css_selector(
        "div.im_history_messages_peer:not(.ng-hide) div.audio_player_actions > a:nth-child(1)")

    for download_audio in audios:
        download_audio.click()

    documents = driver.find_elements_by_css_selector(
        "div.im_history_messages_peer:not(.ng-hide) .im_message_document")

    download_documents = 0
    for document in documents:
        extension_document = document.find_element_by_xpath(".").find_element_by_class_name(
            "im_message_document_name").get_attribute("data-ext")

        if extension_document in EXTENSIONS_DOCUMENT:
            document.find_element_by_css_selector(
                "div.im_message_document_actions > a:nth-child(1)").click()
            download_documents = download_documents + 1

    count_documents = len(audios) + download_documents
    while True:
        if len(os.listdir("{}TmpDownload".format(DOWNLOAD_FOLDER))) == count_documents:
            log.info(f"Загружено {count_documents} документов")
            break
        else:
            time.sleep(0.5)

    for file in os.listdir("{}TmpDownload".format(DOWNLOAD_FOLDER)):
        os.rename("{}TmpDownload\\{}".format(DOWNLOAD_FOLDER, file),
                  path_chat_folder + "\\{}".format(file))
    log.info(f"Загруженные файлы перемещены в {path_chat_folder}")


def screen_chats(driver):
    if not os.path.isdir("{}TmpDownload".format(DOWNLOAD_FOLDER)):
        os.mkdir("{}TmpDownload".format(DOWNLOAD_FOLDER))
        log.info(f"папка {DOWNLOAD_FOLDER}TmpDownload создана")
    chat_number = 0
    while True:
        chat_number = chat_number + 1

        badge_chat = driver.find_element_by_xpath(
            "/html/body/div[1]/div[2]/div/div[1]/div[2]/div/div[1]/ul/li[{}]/a/div[1]/span".format(chat_number))

        if badge_chat.text != "":
            continue

        chat = driver.find_element_by_xpath(
            "/html/body/div[1]/div[2]/div/div[1]/div[2]/div/div[1]/ul/li[{}]".format(chat_number))
        chat.click()
        screen_chat(driver)


if __name__ == "__main__":

    log.info("Начало выполнения программы")
    driver = webdriver.Firefox(create_firefox_profile())
    log.info("Профиль firefox успешно настроен")
    wait = WebDriverWait(driver, 20)
    driver.get(URL)
    screen_object_profile(driver)
    screen_headers_chats(driver)
    screen_chats(driver)
    log.info("Выполнение программы успешно завершено!!!")
