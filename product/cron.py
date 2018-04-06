import json
import requests
from django.db import connection
from django.shortcuts import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages


def get_api_data(request):
    response = requests.get("https://django-shop-test.herokuapp.com/api/")
    json_data = json.loads(response.text)

    for product in json_data:
        title = product['fields']['title']
        description = product['fields']['description']
        price = product['fields']['price']
        amount = product['fields']['amount']
        image = product['fields']['image_url']
        meta_keywords = product['fields']['meta_keywords']
        meta_description = 'meta'
        sku = product['fields']['sku']
        on_the_main = False

        cursor = connection.cursor()

        cursor.execute(("INSERT INTO product_product (title,description,price,quantity,meta_keywords,meta_description,on_the_main,sku,image) "
                        "VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s) ON CONFLICT (sku) DO UPDATE SET id=EXCLUDED.id,title=EXCLUDED.title,"
                        "description=EXCLUDED.description,price=EXCLUDED.price,quantity=EXCLUDED.quantity,meta_keywords=EXCLUDED.meta_keywords,"
                        "meta_description=EXCLUDED.meta_description,on_the_main=EXCLUDED.on_the_main,sku=EXCLUDED.sku, image=EXCLUDED.image"),
                       (title, description, price, amount, meta_keywords, meta_description, on_the_main, sku, image))

    messages.info(request, 'Products updated successfully')

    return HttpResponseRedirect(reverse('account:account'))

