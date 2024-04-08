import requests
from bs4 import BeautifulSoup
import json

file_name = "data.json"
json_data = []
url = 'https://avic.com.ua/macbook/available--on_seriya--pro'

response = requests.get(url)
response.raise_for_status()
soup = BeautifulSoup(response.text, 'html.parser')
items = soup.find_all("div", class_="item-prod")

# get all cards from page
for each_item in items:
    item_data = {}
    item_data["item_title"] = each_item.find("div", class_="card__top").find("a", class_="card__title").text
    item_data["price"] = each_item.find("div", class_="card").find("div", class_="card__bottom").find("div", class_="card__price").find("div", class_="card__price-new").text
    item_data["link_to_page"] = each_item.find("div", class_="card__top").find("a", class_="card__title").get("href")

    # open page with each item with detailed info
    response = requests.get(item_data["link_to_page"])
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')

    item_description = soup.find("div", class_="product-main-section").find("ul", class_="feature-descr").find_all("li", class_="feature-descr__item")
    list_with_item_char = []
    # get characteristics for each item
    for li_element in item_description:
        list_with_item_char.append(li_element.find("div", class_="feature-descr__info").text.strip())
    item_data["characteristics"] = list_with_item_char
    json_data.append(item_data)

with open(file_name, "w") as json_file:
    json.dump(json_data, json_file, ensure_ascii=False, indent=4)
