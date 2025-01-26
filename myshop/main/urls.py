from django.urls import path
from .views import *
urlpatterns = [
    path('',index,name="index"),
    path('blog/',blog,name="blog"),
    path('blog-single',blog_single,name="blog-single"),
    path('cart/',cart,name="cart"),
    path('checkout/',checkout,name="checkout"),
    path('login/',log_in,name="login"),
    path('shop/',shop,name="shop"),
    path('contact/',contact_us,name="contact"),
    path('product-details/<int:id>',product_details,name="product-details"),
    path('profile/',customer_profile,name='profile')
]
