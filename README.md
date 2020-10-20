# TLScreen #

**TLScreen** предназначен для сохранения данных из Telegram аккаунта. Программа последовательно делает **скриншоты** истории чатов и сохраняет медиа файлы на локальный диск.   

## Использование ##

**Обязательные компоненты:**

1. Python не ниже 3.7.7 версии.
2. Последняя версия браузера Mozilla Firefox.
3. geckodriver последней версии.

 **Порядок работы:**

1. Установить зависимости: 

   ` pip install -r requirements.txt`

2. Настроить профиль в  браузере Firefox под которым будет выполняться программа (лучше всего для программы создать отдельный профиль). Для этого:

   - В windows запускаем диалоговое окно **Выполнить** и вводим `firefox - P` (В линуксе вводим это в терминале). Откроется окно **менеджера профилей Firefox**

     

     ![manager_profiles](documents/manager_profiles.jpg)

     

   - Создаём профиль и запускаем браузер от него.

3. Скачиваем geckodriver: https://github.com/mozilla/geckodriver/releases.

4. Выполнить авторизацию в `https://web.telegram.org/#/login`.

5. Настроить параметры работы программы в файле `config.txt`:

   - **GECKODRIVER** - расположение файла `geckodriver.exe`. Обязательный для заполнения.
   - **FIREFOX_PROFILE** - расположение папки созданного профиля. Обязательный для заполнения.
   - **DOWNLOAD_FOLDER** - расположение папки для загрузки данных. Обязательный для заполнения. Папка должна быть создана заранее.
   - **MAX_MESSAGES** - максимальное количество загружаемых сообщений в диалоге (больше тысячи ставить не рекомендуется). По умолчанию: 1000.
   - **EXTENSIONS_DOCUMENT** - расширения файлов для загрузки. Перечисляются через пробел. По умолчанию: [".docx", ".txt"].
   - **SCREEN_UNEAD_MESSAGES** - открывать диалоги с непрочитанными сообщениями. True или False. По умолчанию: False.
   - **SCREEN_GROUP** - сохранять переписку в группах. True или False. По умолчанию: False.
   - **SCREEN_CONTACT** - сохранять переписку в диалогах. True  или False. По умолчанию: False.
   - **SCREEN_CHANNEL** - сохранять переписку в каналах. True или False. По умолчанию: False.
   - **SCREEN_BOT** - сохранять переписку с ботами. True или False. По умолчанию: False.

6. Отключите блокировку экрана по времени, иначе будет скриниться черный экран.

7. Запустить скрипт. Программа сама откроет браузер, начнёт листать диалоги в Телеграм, делать скриншоты и сохранять медиа файлы по папкам. 

   `python main.exe`

## Демонстрация работы программы ##

![video](documents/demonstration.gif)



## Результат работы программы ##

Весь процесс работы программы записывается в файл `info.log`.

Если программа успешно отработает, то в каталоге **DOWNLOAD_FOLDER** будут лежать скриншоты:

- profile.jpg - скриншот основных настроек пользователя.
- active_sessions.jpg - скриншот активных сессий пользователя.
- chats_<i>.jpg - скриншоты заголовков чатов.

Кроме того, для каждого диалога будет создана папка с названием чата. В каждой из этих папок будут лежать скриншоты переписки, голосовые сообщения и медиа файлы, которые были разрешены на скачивание в параметре  **EXTENSIONS_DOCUMENT**.