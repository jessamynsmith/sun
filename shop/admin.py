from django.contrib import admin
from .models import Category,Product,Profile,Service,Purchase

class CategoryAdmin(admin.ModelAdmin):
	list_display = ['name','slug']
	prepopulated_fields = {'slug':('name',)}
admin.site.register(Category,CategoryAdmin)

class ProductAdmin(admin.ModelAdmin):
	list_display = ['name','price','stock','available','created','updated']
	list_editable = ['price','stock','available']
	prepopulated_fields = {'slug':('name',)}
	list_per_page = 20
admin.site.register(Product,ProductAdmin)

class ProfileAdmin(admin.ModelAdmin):
	list_display = ['user','about']
admin.site.register(Profile,ProfileAdmin)

class ServiceAdmin(admin.ModelAdmin):
	list_display = ['name','price', 'available']
	list_editable = ['price', 'available']
admin.site.register(Service,ServiceAdmin)

class PurchaseAdmin(admin.ModelAdmin):
	list_display = ['product','buyer','time']
	list_editable = ['buyer']
admin.site.register(Purchase,PurchaseAdmin)