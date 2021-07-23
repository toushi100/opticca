from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('about/',views.about,name="about"),
    path('login/', auth_views.LoginView.as_view(template_name='main/login.html'), name = 'login'),
    path('logout/',views.logout_,name="logout"),
    path('sign-up/',views.signup,name='signup'),
    path('sign-up/$/',views.signup,name='signup'),
    path('validate-user/$/',views.validate_user,name='validate-user'),#ajav validate user
    path('validate-mail/$/',views.validate_mail,name='validate-mail'),#ajax validate mail
    path('dashboard/', views.dashboard, name='dashboard'),
    path('store/', views.store, name='store'),
    path('store/edit/', views.store_edit, name='edit_store'),
    path('store/edit/$/', views.store_edit, name='edit_store'),
    path('store/<store_id>/', views.store, name='store'),
    path('product/add/',views.addproduct,name='add_product'),
    path('product/search/$/',views.search,name="search"),
    path('product/list/$/',views.product_list,name="search_list"),
    path('product/<str:reference>/', views.product, name='product'),
    path('product/<str:reference>/add', views.add_cart, name='add_cart'),
    path('cart/data/',views.get_cart_data,name="cart_data"),
    path('checkout/',views.checkout,name='checkout'),
    path('opt_data/',views.opt_data,name='opt_data'),
    path('form/add_product',views.data_add_product,name='add_data')

]
