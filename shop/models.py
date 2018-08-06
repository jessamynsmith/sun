from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

class Category(models.Model):
	name = models.CharField(max_length=250, unique=True)
	slug = models.SlugField(max_length=250, unique=True)
	description = models.TextField(blank=True)
	image = models.ImageField(upload_to='category', blank=True)

	class Meta:
		ordering = ('name',)
		verbose_name = 'category'
		verbose_name_plural = 'categories'

	def get_url(self):
		return reverse('shop:products_by_category', args=[self.slug])

	def __str__(self):
		return '{}'.format(self.name)

class Product(models.Model):
	name = models.CharField(max_length=250, unique=True)
	slug = models.SlugField(max_length=250, unique=True)
	description = models.TextField(blank=True)
	category = models.ForeignKey(Category, on_delete=models.CASCADE)
	price = models.DecimalField(max_digits=10, decimal_places=2)
	image = models.ImageField(upload_to='product', blank=True)
	stock = models.IntegerField()
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	available = models.BooleanField(default=True)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)

	class Meta:
		ordering = ('name',)
		verbose_name = 'product'
		verbose_name_plural = 'products'

	def get_url(self):
		return reverse('shop:ProdCatDetail', args=[self.category.slug, self.slug])

	def __str__(self):
		return '{}'.format(self.name)

class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	about = models.CharField(max_length=100)
	address = models.CharField(max_length=100)

	def __str__(self):
		return self.user.username

class Service(models.Model):
	name = models.CharField(max_length=250, unique=True)
	description = models.TextField(blank=True)
	price = models.DecimalField(max_digits=10, decimal_places=2)
	available = models.BooleanField(default=True)

	class Meta:
		ordering = ('name',)
		verbose_name = 'service'
		verbose_name_plural = 'services'

	def __str__(self):
		return '{}'.format(self.name)

class Purchase(models.Model):
	product = models.ForeignKey(Product, on_delete=models.CASCADE)
	buyer = models.ForeignKey(User, on_delete=models.CASCADE)
	time = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.product.name
