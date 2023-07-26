CREATE DATABASE cw;

CREATE TABLE companies
(
    company_id    serial PRIMARY KEY,
    company_name  varchar(50)  NOT NULL,
    description   text,
    link          varchar(200) NOT NULL,
    url_vacancies varchar(200) NOT NULL
);

CREATE TABLE vacancies
(
    vacancy_id    serial PRIMARY KEY,
    company_id    int REFERENCES companies (company_id) NOT NULL,
    title_vacancy varchar(150)                          NOT NULL,
    salary        int,
    link          varchar(200)                          NOT NULL,
    description   text,
    experience    varchar(70)
);

SELECT company_name, COUNT(vacancy_id)
FROM companies
JOIN vacancies USING (company_id)
GROUP BY company_name;

SELECT title_vacancy, company_name, salary, vacancies.link
FROM vacancies
JOIN companies USING (company_id);

SELECT company_name, round(AVG(salary)) AS average_salary
FROM companies
JOIN vacancies USING (company_id)
GROUP BY company_name;

SELECT *
FROM vacancies
WHERE salary > (SELECT AVG(salary) FROM vacancies);

SELECT *
FROM vacancies
WHERE lower(title_vacancy) LIKE '%keyword%'
OR lower(title_vacancy) LIKE '%keyword'
OR lower(title_vacancy) LIKE 'keyword%';