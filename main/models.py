import string
import random
import logging
from enum import Enum, unique

from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.utils.translation import gettext as _

from phonenumber_field.modelfields import PhoneNumberField

logger = logging.getLogger("mylogger")

# Create your models here.
'''
The primary attributes of the default user are:

username
password
email
first_name
last_name
'''


class Person(User):
    DoesNotExist = None
    is_customer = models.BooleanField(_('customer ?'), default=False)
    is_supplier = models.BooleanField(_('supplier ?'), default=False)
    Tel = PhoneNumberField(_('phone number'), null=True, blank=True, unique=True)

    default_shipping_address = models.ForeignKey("Address", null=True, blank=True, default=None,
                                                 verbose_name=_("Default shipping address"),
                                                 related_name="default_shipping_address", on_delete=models.PROTECT)

    default_invoicing_address = models.ForeignKey("Address", null=True, blank=True, default=None,
                                                  verbose_name=_("Default invoice address"),
                                                  related_name="default_invoicing_address", on_delete=models.PROTECT)

    '''
    Rules: 
    1) The person is not Email Verified (ignored)
    2) The person can be Either a customer or/and a supplier
    
    '''

    def create_person(self, username, password, email, firstname, lastname):
        N_User = User.objects.create_user(username, email, password, first_name=firstname, last_name=lastname)
        N_User.save()
        pass


class Address(models.Model):
    MISTER = 'MR'
    MISS = 'MISS'
    MISSES = 'MRS'
    GENDER = (
        (MISTER, 'Monsieur'),
        (MISS, 'Mademoiselle'),
        (MISSES, 'Madame'),
    )
    gender = models.CharField(max_length=4, choices=GENDER, default=MISTER, verbose_name="Gender")
    first_name = models.CharField(max_length=50, verbose_name="FirstName")
    last_name = models.CharField(max_length=50, verbose_name="LastName")
    company = models.CharField(max_length=50, blank=True, verbose_name="Company")
    address = models.CharField(max_length=255, verbose_name="Address")
    additional_address = models.CharField(max_length=255, blank=True, verbose_name="2nd Address")
    postcode = models.CharField(max_length=5, verbose_name="Postal Code")
    city = models.CharField(max_length=50, verbose_name="City")
    phone = models.CharField(max_length=10, verbose_name="Phone number")


class ProductType(models.Model):
    name = models.CharField(max_length=150, verbose_name="Product Type")
    short_desc = models.CharField(max_length=150, verbose_name="Short descrition", blank=True)
    attributs = models.CharField(max_length=150, default="", verbose_name="Product Type")


def gen_str():
    # letters = string.ascii_lowercase
    numbers = string.digits
    return ''.join(random.choice(numbers) for i in range(16))


class Product(models.Model):
    name = models.CharField(max_length=150, verbose_name="Product name")
    reference = models.CharField(verbose_name="reference", max_length=16, default=gen_str, editable=False)
    owner = models.ForeignKey("Person", on_delete=models.PROTECT,blank=True,null=True, verbose_name="Store Owner")
    supplier = models.ForeignKey("Store", null=True, blank=True, default=None, verbose_name="Supplier",
                                 related_name="supplier", on_delete=models.PROTECT)
    description = models.CharField(max_length=400, verbose_name="Product description")
    price = models.FloatField(verbose_name="Price", default=0.00)
    type = models.ForeignKey(ProductType, on_delete=models.PROTECT, null=True, blank=True, default=None)
    city = models.ForeignKey("City", on_delete=models.PROTECT,blank=True,null=True)
    category = models.ForeignKey("Category",on_delete=models.PROTECT, blank=True,null=True)
    TS = models.BooleanField(default=0)

class Product_Image(models.Model):
    reference = models.ForeignKey("Product", null=True, blank=True, default=None, verbose_name="Product's image",
                                  related_name="product", on_delete=models.CASCADE)
    image = models.ImageField()
    image_base64 = models.TextField(default="None")
    image_type = models.IntegerField(default=0)


class Order(models.Model):
    customer = models.ForeignKey("Person", null=True, blank=True, default=None,
                                 verbose_name="Customer",
                                 related_name="customer", on_delete=models.PROTECT)

    Order_creation = models.DateTimeField(verbose_name="Order creation date:")

    total = models.FloatField(verbose_name="Total Order", default=None)


class Order_Line(models.Model):
    product = models.ForeignKey("Product", null=True, blank=True, default=None, verbose_name="Product",
                                on_delete=models.PROTECT)
    quantity = models.IntegerField("Quantity")
    attribut_value = models.CharField(verbose_name="Attribut Details", default="empty", max_length=150)


class Store(models.Model):
    name = models.CharField(verbose_name="Store Name", max_length=75)
    owner = models.ForeignKey("Person", on_delete=models.PROTECT, verbose_name="Store Owner")
    logo = models.ImageField(upload_to='Img/logo/')
    logo1 = models.BinaryField(default=None)
    description = models.CharField(max_length=500, verbose_name="Description")


class CartItem(models.Model):
    item = models.ForeignKey("Product", on_delete=models.CASCADE)
    quantity = models.IntegerField("Quantity", default=0)
    attribut_value = models.CharField(verbose_name="Attribut Details", default="empty", max_length=150)


class Cart(models.Model):
    owner = models.ForeignKey("Person", on_delete=models.PROTECT, verbose_name="Store Owner")
    cartitems = models.ManyToManyField("CartItem")
    total = models.FloatField(verbose_name="Total Order", default=None)


class Category(models.Model):
    name = models.CharField(verbose_name="Category", max_length=50)


class Region(models.Model):
    region = models.CharField(verbose_name="Region", max_length=50)

class City(models.Model):
    name = models.CharField(verbose_name="City", max_length=50)
    region = models.ForeignKey("Region",on_delete=models.PROTECT,verbose_name="region city",default=None)



