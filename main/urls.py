from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    # CMS
    path('manage/', views.ManageAccountView.as_view(), name='manage_account'),
    path('create/', views.AccountFormCreate.as_view(), name='create_account'),
    path('<pk>/image/', views.ProductImageUpdateView.as_view(), name='image_product_update'),
    path('<pk>/update/', views.AccountFormUpdate.as_view(), name='update_account'),
    path('<pk>/delete/', views.AccountFormDelete.as_view(), name='delete_account'),
    # default
    path('', views.category_list, name='category_list'),
    path('about/', views.about, name='about'),
    path('buy_account/', views.buy_account, name='buy_account'),
    path('category/<slug:category_slug>/', views.category_list, name='account_list_by_category'),
    # order
    path('order/product/<int:product_pk>/', views.orders_form, name='order_form'),
    path('product/<int:product_pk>/', views.account_detail, name='account_detail'),
]

