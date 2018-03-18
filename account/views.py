from product.models import Product, Order
from account.models import Bookmark
from django.shortcuts import render, get_object_or_404, HttpResponseRedirect, redirect
from django.contrib import messages
from base.settings import BASE_DIR
import csv
from django.core.files.storage import FileSystemStorage
import json
from django.urls import reverse
from django.db import connection


def get_user_account(request):
    return render(request, 'account/user_account.html')

def get_user_bookmark(request):
    if request.method == 'GET':
        user_id = request.user.id
        products = Bookmark.objects.filter(user_id=user_id)
        product_list = []
        for product in products:
            product = Product.objects.filter(id=product.product_id)
            product_list.append(product)

        context = {
            'bookmarks': product_list
        }
        return render(request, 'account/wishlist.html', context)

def add_bookmark(request):
    if request.method == 'POST':
        p_id = request.POST.get('product_id')
        user_id = request.POST.get('user_id')

        bookmark = Bookmark(product_id=p_id, user_id=user_id)
        bookmark.save()
        messages.info(request, 'Product added to the wishlist')
        return redirect('/')

def get_orders(request):
    if request.method == 'GET':
        user_email = request.user.email
        orders = Order.objects.filter(email=user_email)

        for i in orders:
            i.order_details = json.loads(i.order_details)

        context = {
            'orders': orders
        }

        return render(request, 'account/user_orders.html', context)


def upload_csv(request):
    if request.method == 'POST' and request.FILES['csv_file']:
        csv_file = request.FILES['csv_file']
        fs = FileSystemStorage()
        filename = fs.save(csv_file.name, csv_file)
        uploaded_file_url = BASE_DIR + fs.url(filename)

        with open(uploaded_file_url, 'r') as csvfile:
            productreader = csv.reader(csvfile, delimiter=',', quotechar='|')
            for row in productreader:
                title = row[0]
                description = row[1]
                price = float(row[2])
                quantity = int(row[3])
                meta_keywords = row[4]
                meta_description = row[5]
                sku = row[6]
                on_the_main = False

                cursor = connection.cursor()

                cursor.execute(("INSERT INTO product_product (title,description,price,quantity,meta_keywords,meta_description,on_the_main,sku) "
                                "VALUES (%s,%s,%s,%s,%s,%s,%s,%s) ON CONFLICT (sku) DO UPDATE SET id=EXCLUDED.id,"
                                "title=EXCLUDED.title,description=EXCLUDED.description,price=EXCLUDED.price,quantity=EXCLUDED.quantity,meta_keywords=EXCLUDED."
                                "meta_keywords,meta_description=EXCLUDED.meta_description,on_the_main=EXCLUDED.on_the_main,sku=EXCLUDED.sku"),
                                (title, description, price, quantity, meta_keywords, meta_description, on_the_main, sku))

            messages.info(request, 'File uploaded successfully')

        return HttpResponseRedirect(reverse('account:account'))





