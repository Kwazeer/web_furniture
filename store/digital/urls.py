from django.urls import path
from .views import *

urlpatterns = [
    path('', ProductListView.as_view(), name='main'),
    path('product/<slug:slug>/', ProductDetailView.as_view(), name='product'),
    path('category/<slug:slug>/', ProductByCategoryView.as_view(), name='category'),
    path('search/', SearchView.as_view(), name='search'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('register/', register_view, name='register'),
    path('add_favorite/<slug:slug>/', add_favorite_product, name='add_favorite'),
    path('my_favorites/', FavoriteProductsView.as_view(), name='favorites'),
    path('add_product/<slug:slug>/<str:action>/', control_product_order, name='add_or_delete'),
    path('my_cart/', my_cart_view, name='my_cart'),
    path('delete_cart/', delete_cart, name='delete_cart'),
    path('profile/', profile_view, name='profile'),
    path('edit_profile/', edit_profile_view, name='edit_profile'),
    path('checkout/', checkout_view, name='checkout'),
    path('payment/', create_checkout_session, name='payment'),
    path('success_payment/', success_payment, name='success_payment'),

]
