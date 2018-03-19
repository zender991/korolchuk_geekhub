from django.conf.urls import url

from product.views import index, subcategory_product, product_details, cart, remove_product_from_session, \
    checkout, complete_order, edit_product, save_edited_product, subcategory_product, edit_subcategory, \
    save_edited_subcategory, add_product, add_product_to_db, make_json_api


app_name = 'product'
urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'^(?P<id>\d+)/$', subcategory_product,name='subcategory-product'),
    url(r'^(?P<id>\d+)/details/$', product_details, name='product-details'),
    url(r'^(?P<id>\d+)/edit-product/$', edit_product, name='edit-product'),
    url(r'^(?P<id>\d+)/edit-subcategory/$', edit_subcategory, name='edit-subcategory'),
    url(r'^cart/$', cart, name='cart'),
    url(r'^save-edited-product/$', save_edited_product, name='save-edited-product'),
    url(r'^save-edited-subcategory/$', save_edited_subcategory, name='save-edited-subcategory'),
    url(r'^remove-product/$', remove_product_from_session, name='remove-product'),
    url(r'^checkout/$', checkout, name='checkout'),
    url(r'^complete-checkout/$', complete_order, name='complete-checkout'),
    url(r'^add-product/$', add_product, name='add-product'),
    url(r'^add-product-to-db/$', add_product_to_db, name='add-product-to-db'),
    url(r'^products.json$', make_json_api, name='make-json-api'),
    #url(r'^(?P<id>\d+)/order-products$', subcategory_product, name='order-products'),


]