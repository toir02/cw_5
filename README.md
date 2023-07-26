# Для чего нужен этот проект?

Проект для парсинга компаний и их вакансий с платформы ``HeadHunter`` и последующим сохранением в базу данных.
Используемая СУБД в проекте ``PostgreSQL``.

____

## ERD диаграмма для базы данных

<a href="https://ibb.co/ykpKRYc"><img src="https://i.ibb.co/rp3qtcR/image.png" alt="image" border="0" /></a>

База данных имеет две таблицы:
1) companies (работадели)
2) vacancies (вакансии)

Отношения между таблицами one-to-many (один ко многим).


#### Таблица companies

Колонки:
* company_id (уникальный id компании, автоинкрементирующаяся, тип serial с ограничением PRIMARY KEY, связана с колонкой company_id в таблице vacancies)
* company_name (название компании, тип varchar)
* description (описание компании, тип text)
* link (ссылка на компанию, тип varchar)
* url_vacancies (ссылка на вакансии компании, тип varchar)

### Таблица vacancies
