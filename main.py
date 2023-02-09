
import time
from fake_useragent import UserAgent
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import logging
from random import randrange
from seleniumwire import webdriver
from webdriver_manager.chrome import ChromeDriverManager


def generate_fake_ua() -> UserAgent:
    ua = UserAgent()
    return ua.random


def get_keywords_list(queryList: list) -> list:
    keywords = []
    if not queryList:
        logging.exception("QueryList is null")
        exit(1)

    for query in queryList:
        keywords.append(query.lower().replace(" ", "+"))

    return keywords


def get_position(domain_list: list, keywords: list) -> list:
    options = Options()
    options.page_load_strategy = 'normal'
    browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    href_dict = {}
    result = []
    next_page_link = []
    DOMAIN = 'webcache.googleusercontent.com'
    for page in range(1,4):
        count = 0
        for keyword in keywords:
            url = 'https://www.google.com/search?q=' + keyword if page < 3 else next_page_link[count]
            try:
                browser.get(url)
                if page == 2:
                    print("----------------")
                    print(count)
                    print("----------------")
                    browser.get(url)
                    next_page_link.append(browser.find_element(By.XPATH, '//td[@class="d6cvqb BBwThe"]//a[@id="pnnext"]').get_attribute(
                            'href'))
                    browser.get(next_page_link[count])
                    print(f"Count: {count} url: {next_page_link[count]}")

                elif page == 3:
                    print("----------------")
                    print(count)
                    print("----------------")
                    browser.get(url)
                    next_page_link = browser.find_element(By.XPATH, '//td[@class="d6cvqb BBwThe"]//a[@id="pnnext"]').get_attribute(
                            'href')
                    browser.get(next_page_link)
                    print(f"Count: {count} url: {next_page_link[count]}")

                dns = browser.find_elements(By.XPATH, '//div[@class="yuRUbf"]//a')
                href_dict = {i + 1: dns[i].get_attribute('href') for i in range(0, len(dns))}
            except Exception as ex:
                    logging.exception(ex)

            count += 1
            href_dict = check_for_webcache(href_dict, DOMAIN)# словарь с сайтами без рекламы
            print(f"Page is: {page}")
            for key, value in href_dict.items():
                 print(f"{key} : {value}")

            dict_res = {}
            for domain in domain_list:
                for key,value in href_dict.items():
                    if value.startswith(domain, 8):
                      dict_res[key] = value

            result.append(dict_res)
            time.sleep(randrange(2,5))  # пауза между запросами, спасение от бана или капчи
    if browser:
        browser.quit()
    return result


def check_for_webcache(href_dict: dict, domain: str) -> dict:
    href_dict = {key: value for key, value in href_dict.items() if not value.startswith(domain, 8)}
    return href_dict


def main():
    query_list  =  [
        'кухни зов ',
        'купить кухни'
        ]

    domain_list = [
            'zov01.ru',
            'zov-krasnodar.ru',
            'maikop.mebelister.ru',
            'zovmoscow.ru',
            'zovrus.ru',
            'leroymerlin.ru',
            'mebelveb.ru'
     ]

    region_title = 'Краснодар'
    result = get_position(domain_list, get_keywords_list(query_list))
    print('Позиция сайта на странице:')
    print(result) # TODO: вывод в формате json


main()
'/search?q=%D0%BA%D1%83%D0%BF%D0%B8%D1%82%D1%8C+%D0%BA%D1%83%D1%85%D0%BD%D0%B8&amp;sxsrf=AJOqlzUCAQmMA1BOet2nsJfeFgx6l9sXJw:1675961921004&amp;ei=QCblY4v6PJuIxc8PzOWqmAg&amp;start=20&amp;sa=N&amp;ved=2ahUKEwiLmtXX9Ij9AhUbRPEDHcyyCoM4ChDw0wN6BAgFEBc&amp;cshid=1675962084698591'

