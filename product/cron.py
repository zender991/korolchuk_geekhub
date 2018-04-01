import json
import requests
from django.db import connection
from django.shortcuts import render, get_object_or_404, HttpResponseRedirect, redirect
from django.urls import reverse


def get_api_data(request):
    # response = requests.get("https://django-shop-test.herokuapp.com/api/")
    # json_data = json.loads(response.text)
    #
    # for product in json_data:
    #     title = product['fields']['title']
    #     description = product['fields']['description']
    #     price = product['fields']['price']
    #     image_url = product['fields']['image_url']
    #     meta_tags = product['fields']['meta_tags']
    #
    # cursor = connection.cursor()
    #
    # cursor.execute((
    #                    "INSERT INTO product_product (title,description,price,quantity,meta_keywords,meta_description,sku) "
    #                    "VALUES (%s,%s,%s,%s,%s,%s,%s,%s) ON CONFLICT (sku) DO UPDATE SET id=EXCLUDED.id,"
    #                    "title=EXCLUDED.title,description=EXCLUDED.description,price=EXCLUDED.price,quantity=EXCLUDED.quantity,meta_keywords=EXCLUDED."
    #                    "meta_keywords,meta_description=EXCLUDED.meta_description,sku=EXCLUDED.sku"),
    #                (title, description, price, quantity, meta_keywords, meta_description, sku))

    # messages.info(request, 'Products updated successfully')

    return HttpResponseRedirect(reverse('account:account'))

