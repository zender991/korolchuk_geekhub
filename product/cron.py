import json
import requests


def get_api_data():
    response = requests.get("https://django-shop-test.herokuapp.com/api/")
    json_data = json.loads(response.text)
    success = True

    for product in json_data:
        title = product['fields']['title']
        description = product['fields']['description']
        price = product['fields']['price']
        image_url = product['fields']['image_url']
        meta_tags = product['fields']['meta_tags']

    return success

