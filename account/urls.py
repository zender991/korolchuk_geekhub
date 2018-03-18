from django.conf.urls import url
from account.views import get_user_bookmark, get_user_account, add_bookmark, get_orders, upload_csv

app_name = 'account'


urlpatterns = [

    url(r'^$', get_user_account, name='account'),
    url(r'^wishlist/$', get_user_bookmark, name='wishlist'),
    url(r'^add-to-wishlist/$', add_bookmark, name='add-bookmark'),
    url(r'^user-orders/$', get_orders, name='user_orders'),
    url(r'^upload-csv/$', upload_csv, name='upload-csv')
]