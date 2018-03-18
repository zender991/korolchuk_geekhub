import csv
from product.models import Product

with open('test.csv', 'r') as csvfile:
    productreader = csv.reader(csvfile, delimiter=',', quotechar='|')
    for row in productreader:
        title = row[0]
        description = row[1]
        price = row[2]
        quantity = row[3]
        meta_keywords = row[4]
        meta_description = row[5]

        product = Product(title=title, description=description, price=price, quantity=quantity,
                          meta_keywords=meta_keywords, meta_description=meta_description)
        product.save()
