# Для чего нужен этот проект?

Проект для парсинга компаний и их вакансий с платформы ``HeadHunter`` через API и последующим сохранением в базу данных.
Используемая СУБД в проекте ``PostgreSQL``.

____

## База данных

### ERD диаграмма для базы данных

<a href="https://ibb.co/ykpKRYc"><img src="https://i.ibb.co/rp3qtcR/image.png" alt="image" border="0" /></a>

База данных имеет две таблицы:
1) companies (работадели)
2) vacancies (вакансии)

Отношения между таблицами one-to-many (один ко многим).


#### Таблица companies

Колонки:
* company_id (уникальный id компании, автоинкрементирующийся, тип serial с ограничением PRIMARY KEY, связана с колонкой company_id в таблице vacancies)
* company_name (название компании, тип varchar)
* description (описание компании, тип text)
* link (ссылка на компанию, тип varchar)
* url_vacancies (ссылка на вакансии компании, тип varchar)

#### Таблица vacancies

Колонки:
* vacancy_id (уникальный id вакансии, автоинкрементирующийся, тип serial с ограничением PRIMARY KEY)
* company_id (уникальный id компании, тип int, связан с колонкой company_id в таблице companies)
* title_vacancy (название вакансии, тип varchar)
* salary (зарплата, указанная в вакансии, тип int)
* link (ссылка на вакансию, тип varchar)
* description (описание вакансии, тип text)
* experience (требуемый опыт в вакансии, тип varchar)

____
### Как использовать данный проект?
