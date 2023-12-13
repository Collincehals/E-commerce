from django.urls import path
from . import views

urlpatterns =[
    path('', views.homepage, name='homepage'),
    path('category/<tag>/', views.homepage, name='category'),
    path('post/product/', views.create_product, name='create-product'),
    path('shop/', views.shop, name='shop'),
    path('product/<pk>/', views.product_details, name='product-details'),
    path('blog/', views.blog, name='blog'),
    path('blog/details/', views.blog_details, name='blog-details'),
    path('contact/', views.contact, name='contact'),
    path('shopping/cart/', views.shopping_cart, name='shopping-cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('update_item/', views.update_item, name='update-item'),
    path('process_order/', views.processOrder, name='process-order'),
    path('dashboard/', views.admin_dashboard, name='admin-dashboard'),
]