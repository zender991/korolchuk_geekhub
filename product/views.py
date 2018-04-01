from django.shortcuts import render, get_object_or_404, HttpResponseRedirect, redirect
from django.contrib import messages
from product.models import Product, Subcategory, Order, Currency
from product.forms import CheckoutFormValidation, AddProductFormValidation
from django.utils.datastructures import MultiValueDictKeyError
import json
from django.urls import reverse
from django.core import serializers
from django.http import HttpResponse
from product.send_email import send_email


def index(request):
    context = {
        'products': Product.objects.filter(on_the_main=True)
    }
    return render(request, 'product/index.html', context)


def subcategory_product(request, id):
    context = {
        'subcategory': get_object_or_404(Subcategory, id=id)
    }
    return render(request, 'product/subcategory-product.html', context)


def product_details(request, id):
    context = {
        'product': get_object_or_404(Product, id=id)
    }
    return render(request, 'product/product-details.html', context)


def add_product_to_session(request, p_id, quantity):
    request.session.modified = True
    if 'products' not in request.session:
        request.session['products'] = []

    if len(request.session['products']) == 0:
        request.session['products'].append(
            {'product_id': p_id,
             'quantity': quantity
             }
        )
        messages.info(request, 'Added to cart!')
    else:
        for product in request.session['products']:
            if product.get('product_id') == p_id:
                product['quantity'] = int(product['quantity']) + int(quantity)
                messages.info(request, 'Added to cart!')

        id_list_in_session = []
        for product in request.session['products']:
            id_list_in_session.append(product.get('product_id'))

        if p_id not in id_list_in_session:
            request.session['products'].append(
                {'product_id': p_id,
                 'quantity': quantity
                 }
            )
            messages.info(request, 'Added to cart!')


def cart(request):
    if request.method == 'POST':
        form = AddProductFormValidation(request.POST)
        if not form.is_valid():
            received_request = request.POST
            next_page = received_request.get('next', '/')
            p_id = received_request.get('product_id')
            quantity = received_request.get('quantity')
            add_product_to_session(request, p_id, quantity)
            return HttpResponseRedirect(next_page)
        else:
            messages.info(request, 'Wrong input parameters')
            return redirect('/')

    else:
        if request.session.get('products'):
            all_products = []
            for item in request.session.get('products'):
                p_id = item.get('product_id')
                quantity = item.get('quantity')
                product = Product.objects.filter(id=p_id)
                for pr in product:
                    product_title = pr.title
                    product_price = pr.price

                product_dict = {
                    'id': p_id,
                    'title': product_title,
                    'price': product_price,
                    'quantity': quantity
                }

                all_products.append(product_dict)

            subtotal = 0
            for product in all_products:
                subtotal = subtotal + (product.get('price') * int(product.get('quantity')))

            if 'subtotal' not in request.session:
                request.session['subtotal'] = []
            request.session['subtotal'] = subtotal

            return render(request, 'product/cart.html', {'products': all_products, 'subtotal': subtotal})

        else:
            return render(request, 'product/cart.html')


def remove_product_from_session(request):
    if request.method == 'POST':
        request.session.modified = True
        p_id = request.POST.get('product_id')

        for product in request.session['products']:
            if product.get('product_id') == str(p_id):
                request.session['products'].remove(product)

        messages.info(request, 'Product removed from cart!')

        return HttpResponseRedirect(reverse('product:cart'))


def checkout(request):
    request.session.modified = True
    for product in request.session['products']:
        db_product = Product.objects.filter(id=product.get('product_id'))
        for item in db_product:
            title = item.title
            price = item.price
        product['title'] = title
        product['price'] = price

    context = {
        'orders': request.session['products'],
        'subtotal': request.session['subtotal']
    }

    return render(request, 'product/checkout.html', context)


def complete_order(request):
    if request.method == 'POST':
        form = CheckoutFormValidation(request.POST, request.FILES)
        if form.is_valid():

            request.session.modified = True
            received_request = request.POST
            name = received_request.get('name')
            email = received_request.get('email')
            subtotal = request.session['subtotal']
            products = json.dumps(request.session['products'])
            order = Order(name=name, email=email, subtotal=subtotal, order_details=products)
            order.save()

            html_product_list = ""

            currency = Currency.objects.get(title='hrn')
            currency_rate = currency.value
            email_subtotal = subtotal * currency_rate

            for product in request.session['products']:
                html_product_list += "<ul><li>" + product.get('title') + "</li><li>Price - " + str((product.get('price'))* currency_rate) \
                                     + "</li><li>Quantity - " + str(product.get('quantity')) + "</li></ul><hr>"

            #send_email(name, email_subtotal, html_product_list)

            del request.session['products']
            del request.session['subtotal']
            messages.info(request, 'Order created successfully')
        else:
            messages.info(request, 'Wrong input parameters')
            return HttpResponseRedirect(reverse('product:checkout'))

    return HttpResponseRedirect(reverse('product:index'))


def edit_product(request, id):
    context = {
        'product': get_object_or_404(Product, id=id)
    }
    return render(request, 'product/edit-product.html', context)


def edit_subcategory(request, id):
    context = {
        'subcategory': get_object_or_404(Subcategory, id=id)
    }
    return render(request, 'product/edit-subcategory.html', context)


def save_edited_product(request):

    if request.method == 'POST':
        p_id = request.POST.get('product_id')
        title = request.POST.get('product_title')
        description = request.POST.get('product_description')
        quantity = request.POST.get('product_quantity')
        meta_keywords = request.POST.get('product_meta_keywords')
        meta_description = request.POST.get('product_meta_description')
        price = request.POST.get('product_price')
        try:
            image = request.FILES['product_image']
        except MultiValueDictKeyError:
            image = request.POST.get('product_image_hidden')

        edited_product = Product.objects.get(id=p_id)
        edited_product.title = title
        edited_product.description = description
        edited_product.quantity = quantity
        edited_product.image = image
        edited_product.meta_keywords = meta_keywords
        edited_product.meta_description = meta_description
        edited_product.price = price

        edited_product.save()
        return HttpResponseRedirect(reverse('product:product-details', args=(p_id, )))


def save_edited_subcategory(request):
    if request.method == 'POST':
        subcategory_id = request.POST.get('subcategory_id')
        title = request.POST.get('subcategory_title')

        edited_subcategory = Subcategory.objects.get(id=subcategory_id)
        edited_subcategory.title = title
        edited_subcategory.save()

        return HttpResponseRedirect(reverse('product:subcategory-product', args=subcategory_id))


def order_products(request):
    if request.method == 'POST':
        if request.POST.get('order_by') == 'asc':
            products = Product.objects.all().order_by('price')

            context = {
                'subcategory': products
            }

            print(context)

            return redirect('/')
        elif request.POST.get('order_by') == 'desc':
            products = Product.objects.all().order_by('-price')

            context = {
                'subcategory': products
            }

            print(context)

            return HttpResponseRedirect(reverse('product:index'))


def add_product(request):
    return render(request, 'product/add-product.html')


def add_product_to_db(request):
    if request.method == 'POST' and request.FILES['product_image']:
        title = request.POST.get('product_title')
        description = request.POST.get('product_description')
        quantity = request.POST.get('product_quantity')
        image = request.FILES['product_image']
        sku = request.POST.get('product_sku')
        price = request.POST.get('product_price')

        meta_description = "Buy best price free shipping %s  discount" % title

        product = Product(title=title, description=description, quantity=quantity, image=image, sku=sku, price=price,
                          meta_keywords=title, meta_description=meta_description)
        product.save()

        return HttpResponseRedirect(reverse('account:account'))



def make_json_api(request):
    products = Product.objects.all()
    jsondata = serializers.serialize('json', products)
    return HttpResponse(jsondata, content_type="application/json")

