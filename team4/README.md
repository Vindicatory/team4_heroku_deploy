# Сайт для ведения промо-кампаний

## Project Structure

```bash
.
|-- pr

    |-- components - Регистрация пользователя
        | auth.py - LoginUser
        | query.py - вспомогательные запросы
    |-- keys - Подключение к базе данных
        | key.txt - строка доступ к базе данных
    |-- models - Структура базы данных
        | __init__.py
        | database_structure.md
        | users.py - База данных users
        | campaigns.py - База данных campaigns
        | user_campaigns.py - База данных user_campaigns
        | adresses.py - База данных adresses
        | campaign_adresses.py - База данных campaign_adresses
        | visits.py - База данных visits
    |-- pycodestyle_check
        | pycodestyle.py - проверка кода на стандарт PEP
    |-- static - css templates
    |-- queries - SQL запросы
    |-- templates - HTML формы
        | base.html - базовый шаблон
        | sign_up.html - страница для входа пользователя по логину и паролю
        | sign_in.html - страница для регистрации нового пользователя
        | main_page.html - главная страница входа пользователя, список кампаний
        | create_campaign.html - страница создания новой кампании
        | edit_campaign.html - страница отдельной кампании | добавление пользователя в кампанию
        | visits.html - страница с добавлением информации о посещениях
    |-- templates_backup -- html формы, Bootstrap шаблоны
    |-- templates_test - Bootstrap шаблоны
    |-- views - View формы
        | hello.py - View-форма: главная страница
        | login.py - View-форма: проверка логина пользователя
        | logout.py - View-форма: logout пользователя
        | sing_up.py - View-форма: регистрация пользователя
        | createcampaign.py - View-форма: создание кампании
        | edit_campaign.py - View-форма: добавление пользователя в кампанию, добавление адресов
        | visit.py -- View-форма: посещение по адресу

    |app.py - главное приложение
|.gitignore
|README.md
