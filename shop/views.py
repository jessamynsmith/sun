from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.http import HttpResponse
from .models import Category,Product,Profile,Service,Purchase
from django.core.paginator import Paginator, EmptyPage, InvalidPage
from django.contrib.auth.models import Group, User
from .forms import ProductForm
from .forms import SignUpForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required


def index(request):
	text_var = 'This is my first django app web page.'
	return HttpResponse(text_var)

#Category view

def allProdCat(request, c_slug=None):
	c_page = None
	products_list = None
	if c_slug!=None:
		c_page = get_object_or_404(Category,slug=c_slug)
		products_list = Product.objects.filter(category=c_page,available=True)
	else:
		products_list = Product.objects.all().filter(available=True)
	'''Pagination code'''
	paginator = Paginator(products_list, 6)
	try:
		page = int(request.GET.get('page','1'))
	except:
		page = 1
	try:
		products = paginator.page(page)
	except (EmptyPage,InvalidPage):
		products = paginator.page(paginator.num_pages)
	return render(request,'shop/category.html',{'category':c_page,'products':products})

def ProdCatDetail(request,c_slug,product_slug):
	try:
		product = Product.objects.get(category__slug=c_slug,slug=product_slug)
	except Exception as e:
		raise e
	return render(request,'shop/product.html', {'product':product})

@login_required(login_url="/")
def CreateProduct(request):
	error = ''
	if request.method == 'POST':
		product_form = ProductForm(request.POST, request.FILES)
		if product_form.is_valid():
			product = product_form.save(commit=False)
			product.user = request.user
			product.save()
			products = Product.objects.filter(user=request.user)
			return render(request, 'shop/my_products.html', {'products':products})
		else:
			error = "Data is not valid"
	product_form = ProductForm()
	return render(request, 'shop/create_product.html', {'product_form': product_form, 'error': error})


@login_required(login_url="/")
def MyProducts(request):
	products = Product.objects.filter(user=request.user)	
	return render(request, 'shop/my_products.html', {'products':products})



@login_required(login_url="/")
def EditProduct(request, product_slug):
    try:
        product = Product.objects.get(slug=product_slug)
        error = ''
        if request.method == 'POST':
            product_form = ProductForm(request.POST, request.FILES, instance=product)
            if product_form.is_valid():
                product_form.save()
                return redirect('http://127.0.0.1:8000/shop/my_products/')
            else:
                error = "Data is not valid"
        else:
           # create and edit form when request is GET
           product_form = ProductForm(instance=product)

        # add `product_form` in context instead of `product`
        return render(request, 'shop/edit_product.html', {'product_form':product_form, 'error':error})
    except Product.DoesNotExist:
        return redirect('/')


















#@login_required(login_url="/")
#def EditProduct(request, c_slug, product_slug):
#	try:
#		product = Product.objects.get(category__slug=c_slug, slug=product_slug)
#		error = ''
#		if request.method == 'POST':
#			product_form = ProductForm(request.POST, request.FILES, instance=product)
#			if product_form.is_valid():
#				product.save()
#				return redirect('shop/my_products.html/')
#			else:
#				error = "Data is not valid"
#
#		return render(request, 'shop/edit_product.html', {'product':product, 'error':error})
#	except Product.DoesNotExist:
#		return redirect('/')

@login_required(login_url="/")
def profile(request, username):
	if request.method == 'POST':
		profile = Profile.objects.get(user=request.user)
		profile.about = request.POST['about']
		profile.save()
	else:
		try:
			profile = Profile.objects.get(user__username=username)
		except Profile.DoesNotExist:
			return redirect('/')
	try:
		profile = Profile.objects.get(user__username=username)
	except Profile.DoesNotExist:
		pass

	products = Product.objects.filter(user=profile.user)
	return render(request, 'accounts/profile.html', {"profile": profile, "products":products})

@login_required(login_url="/")
def signupView(request):
	if request.method == 'POST':
		form = SignUpForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data.get('username')
			signup_user = User.objects.get(username=username)
			customer_group = Group.objects.get(name='Customer')
			customer_group.user_set.add(signup_user)
	else:
		form = SignUpForm()
	return render(request, 'accounts/signup.html', {'form':form})

def signinView(request):
	if request.method == 'POST':
		form = AuthenticationForm(data=request.POST)
		if form.is_valid():
			username = request.POST['username']
			password = request.POST['password']
			user = authenticate(username=username, password=password)
			if user is not None:
				login(request, user)
				return redirect('shop:allProdCat')
			else:
				return redirect('signup')
	else:
		form = AuthenticationForm()
	return render(request,'accounts/signin.html', {'form':form })

def signoutView(request):
	logout(request)
	return redirect('signin')