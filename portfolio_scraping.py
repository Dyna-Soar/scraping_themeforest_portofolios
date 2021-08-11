import csv
import requests
from bs4 import BeautifulSoup
from csv import DictWriter

url = "https://themeforest.net/category/site-templates/personal?sort=sales&tags=portfolio#content"


def main(url):
    portfolios_data = []
    one_page_portfolios_data = get_list_portfolios_info_one_page(url)
    portfolios_data.extend(one_page_portfolios_data)
    for index_page in range(2, 21):
        url_page = build_url_page_portfolios(index_page)
        page_portfolios_data = get_list_portfolios_info_one_page(url_page)
        portfolios_data.extend(page_portfolios_data)
    #print(portfolios_data)
    build_excel_sheet(portfolios_data)


def build_excel_sheet(portfolios_data):
    with open('portfolios_themes.csv', 'w') as outfile:
        writer = DictWriter(outfile, ('name', 'url', 'price'))
        writer.writeheader()
        writer.writerows(portfolios_data)


def build_url_page_portfolios(index_page):
    """Return the url of the asked page"""
    base_url = ["https://themeforest.net/category/site-templates/personal?", "sort=sales&tags=portfolio#content"]
    additional_page = "page=" + str(index_page) + "&"
    url_page = base_url[0] + additional_page + base_url[1]
    return url_page


def get_list_portfolios_info_one_page(url):
    """Return a list of 30 dictionaries of portfolios from a one page of portfolios"""
    list_cards_portfolio = get_list_portfolios_cards(url)
    one_page_portfolios_data = []
    for i in range(30):
        try:
            first_portfolio = get_unique_portfolio_card(list_cards_portfolio, i)
            portfolio_data = extract_infos_portfolio(first_portfolio)
            one_page_portfolios_data.append(portfolio_data)
        except IndexError:
            pass
    return one_page_portfolios_data


def get_list_portfolios_cards(url):
    """Get a list of all portfolio url"""
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    list_cards_portfolio = []
    # Append the div of 30 portfolio cards into a list
    for i in range(30):
        try:
            url_portfolio = soup.findAll("div", class_="shared-item_cards-card_component__root")[i]
            list_cards_portfolio.append(url_portfolio)
        except IndexError:
            pass
    return list_cards_portfolio


def get_unique_portfolio_card(list_portfolios, index):
    """Return the the portfolio content of a list"""
    return list_portfolios[index]


def extract_infos_portfolio(portfolio_card):
    """Return the name, url, and price of a portfolio"""
    try:
        infos_portfolio = portfolio_card.find("a", class_="shared-item_cards-item_name_component__itemNameLink")
        name = infos_portfolio.text
        url = str(infos_portfolio).split('href="')[1].split('" tabindex')[0]
        infos_portfolio2 = portfolio_card.find("div", class_="shared-item_cards-price_component__root")
        price = int(infos_portfolio2.text.strip().split("$")[1])
        portfolio_data = {"name": name, "url": url, "price": price}
        return portfolio_data
    except IndexError:
        pass


main(url)


class Portfolio:
    def __init__(self, name, url, price):
        self.name = name
        self.url = url
        self.price = price
