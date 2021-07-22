from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Person
from .models import Person,Address,ProductType,Product_Image,Order,Order_Line,Store,CartItem,Cart,Category,Region,City
# Register your models here.
admin.site.register(Person)
admin.site.register(Address)
admin.site.register(ProductType)
admin.site.register(Product_Image)
admin.site.register(Order)
admin.site.register(Order_Line)
admin.site.register(Store)
admin.site.register(CartItem)
admin.site.register(Cart)
admin.site.register(Region)
admin.site.register(City)
admin.site.register(Category)
