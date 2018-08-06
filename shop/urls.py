from django.urls import path
from . import views

app_name='shop'

urlpatterns = [

	path('profile/<username>/', views.profile, name='profile'),
	path('create_product/', views.CreateProduct, name='Create_Product'),
	path('my_products/', views.MyProducts, name='My_Products'),
	path('<slug:product_slug>/edit_product/', views.EditProduct, name='Edit_Product'),
	path('', views.allProdCat, name='allProdCat'),
	path('<slug:c_slug>/', views.allProdCat, name='products_by_category'),
	path('<slug:c_slug>/<slug:product_slug>/', views.ProdCatDetail, name='ProdCatDetail'),
]