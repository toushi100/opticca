import logging

from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse,HttpResponseRedirect
from django.http.response import Http404
from django.shortcuts import render, redirect
from django.urls import reverse
from django.core.paginator import Paginator
from django.core.serializers import serialize
from .forms import UserRegisterForm

from main.models import *

logger = logging.getLogger("mylogger")


# Create your views here.

@login_required
def index(request):
    return render(request, 'main/index.html')


def opt_data(request):
    data = {}
    region = list(Region.objects.all().values())

    city = list(City.objects.all().values())
    category = list(Category.objects.all().values())

    data["region"] = region
    data["city"] = city
    data["category"] = category
    return JsonResponse(data)


def about(request):
    return render(request, 'main/about.html')


def signup(request):
    if request.method == 'GET':
        form = UserRegisterForm()
        context = {'form':form}
        return render(request, 'main/signup.html', context)
    elif request.method == "POST":
        # data = request.POST.copy()
        # firstname = data.get('firstname')
        # lastname = data.get('lastname')
        # username = data.get('username')
        # mail = data.get('mail')
        # pwd = data.get('pass')
        # user = Person.objects.create_user(username, mail, pwd)
        # user.first_name = firstname
        # user.last_name = lastname
        # user.save()
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}')
            return redirect('/')
        return render(request, 'main/signup.html', {'form': form})
    return Http404("We don't support this http verb")


def signin(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            logout(request)
            return redirect('/')
        else:
            data = {}
            data['Page'] = 'Connection'
            return render(request, 'main/login.html', data)
    elif request.method == "POST":
        data = request.POST.copy()
        mail = data.get('mail')
        pwd = data.get('pass')
        logged = False
        try:
            user = Person.objects.get(email=mail)
            user = authenticate(username=user.username, password=pwd)
            if user is not None:
                login(request, user)
                logged = True

        except Person.DoesNotExist:
            messages.info(request, 'Votre adresse E-mail/ Mot de passe sont incorrects')
            return render(request, 'main/login.html')

        logger.info("Debug : " + str(mail) + "\n" + str(pwd) + "\n" + str(logged))
        if not logged:
            messages.info(request, 'Votre adresse E-mail/ Mot de passe sont incorrects')
            logger.info("Logged Not")
            return redirect('/login/')
        else:
            logger.info("Logged  in")
            return redirect('/')


def validate_user(request):
    username = request.GET.get('username', None)
    data = {
        'is_taken': Person.objects.filter(username__iexact=username).exists()
    }
    return JsonResponse(data)
    pass


def validate_mail(request):
    mail = request.GET.get('mail', None)
    data = {
        'is_taken': Person.objects.filter(email__iexact=mail).exists()
    }
    return JsonResponse(data)
    pass


def get_cart_data(request):
    if not request.user.is_authenticated:
        return None;
    cart = Cart.objects.filter(owner=Person.objects.filter(username=request.user.username)[0])[0]
    cart_items = cart.cartitems
    cart_items = list(cart_items.all().values())
    for i in cart_items:
        pro = Product.objects.get(id=i["item_id"])
        i["name"] = pro.name
        del i["item_id"]

    data = {
        'total': cart.total
    }
    data['cart_items'] = cart_items
    return JsonResponse(data)
    pass


@login_required
def dashboard(request):
    context = {}
    owner = Person.objects.get(username=request.user)
    store = Store.objects.get(owner=owner)
    product_list = Product.objects.filter(supplier=store)
    context["product_c"] = product_list.count()
    context["order_c"] = Order_Line.objects.filter(product__in=product_list).count()

    return render(request, 'dashboard/dashboard.html', context)
    pass


@login_required()
def store(request, store_id=None):
    data = {}
    store = {}
    owner = Person.objects.get(username=request.user)
    try:
        store = Store.objects.get(owner=owner)

    except ObjectDoesNotExist:
        store = None

    data['store'] = store
    data['products'] = Product.objects.filter(supplier=store)

    return render(request, "store/store.html", data)


@login_required()
def store_edit(request):
    if request.method == "GET":
        store = {}
        try:
            store = Store.objects.get(owner=Person.objects.get(username=request.user))
            data = {}
            data['store'] = store
            return render(request, 'store/store-edit.html', data)
        except ObjectDoesNotExist:
            store = None
            return render(request, 'store/store-edit.html')
    elif request.method == "POST":
        data = request.POST.copy()
        name = data.get('name')
        description = data.get('description')
        logo = request.FILES.get('logo')
        owner = Person.objects.get(username=request.user)
        try:
            store = Store.objects.get(owner=request.user)
            if name: store.name = name
            if description: store.description = description
            if logo: store.logo = logo

            return redirect('/store/')
        except ObjectDoesNotExist:
            store = Store.objects.create(name=name, owner=owner, description=description, logo=logo)
        finally:
            store.save()

        return redirect('/store/')
        pass
    pass


@login_required()
def logout_(request):
    logout(request)
    return redirect('/login/')


def search(request):
    if request.method == "GET":
        data = request.GET.copy()
        text_search = data.get("input", None)
        if len(text_search) < 3:
            return JsonResponse({})
        type = data.get("type")
        location = data
        data_ = {}
        product_list = None
        city_id = int(data.get('city'))
        category_id = int(data.get('category'))
        if category_id == 0 and city_id == 0:
            product_list = Product.objects.filter(name__icontains=text_search)[:7]
        elif category_id == 0:
            city = City.objects.get(id=city_id)
            product_list = Product.objects.filter(name__icontains=text_search, city=city)[:7]
        elif city_id == 0:
            category = Category.objects.get(id=category_id)
            product_list = Product.objects.filter(name__icontains=text_search, category=category)[:7]
        else:
            city = City.objects.get(id=city_id)
            category = Category.objects.get(id=category_id)
            product_list = Product.objects.filter(name__icontains=text_search, city=city, category=category)[:7]
        for i, product in enumerate(product_list):
            if len(product.description) > 75:
                product.description = product.description[1:75]
                product.description += "..."

            Product_name = "product_" + str(i)
            data_[Product_name] = {
                "name": product.name,
                "desc": product.description,
                "reference": product.reference
            }

        return JsonResponse(data_)

    pass


@login_required()
def product_list(request):
    if request.method == "GET":
        data = request.GET.copy()
        text_search = data.get("search")
        print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++",
        "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
        print(text_search)
        page_num = data.get("page")
        if page_num is None:
            page_num = 1
        type = data.get("type")
        location = data
        data_ = {}
        product_list = None
        city_id = int(data.get('city'))
        category_id = int(data.get('category'))
        if category_id == 0 and city_id == 0:
            product_list = Product.objects.filter(name__icontains=text_search)
        elif category_id == 0:
            city = City.objects.get(id=city_id)
            product_list = Product.objects.filter(name__icontains=text_search, city=city)
        elif city_id == 0:
            category = Category.objects.get(id=category_id)
            product_list = Product.objects.filter(name__icontains=text_search, category=category)
        else:
            city = City.objects.get(id=city_id)
            category = Category.objects.get(id=category_id)
            product_list = Product.objects.filter(name__icontains=text_search, city=city, category=category)
        # add image first
        for i in product_list:
            try:
                img = Product_Image.objects.filter(reference_id__exact=i.id)[:1].get()
                i.img = img
            except:
                i.img = 'None'



        pages_handler = Paginator(product_list, 20)
        product_list = pages_handler.page(page_num)

        context = {
            "product_list": product_list,
            

        }
        return render(request, "product/search_list.html", context)


def get_img(product_list,img_list):
    return None


@login_required()
def add_cart(request, reference):
    # check if there is a cart
    """
    1) check if there is a cart for the user. if there isn't create one
    2) add item to cart
    3)save

    :param request:
    :param reference:
    :return:
    """
    quantity = None
    if request.method != "POST":
        return render(request, "product/notfound.html")
    if request.method == "POST":
        data = request.POST.copy()
        quantity = data.get("qtt")

    cart = None
    try:
        owner = Person.objects.get(username=request.user)
        cart = Cart.objects.get(owner=owner)
    except ObjectDoesNotExist:
        cart = Cart()
        cart.owner = Person.objects.get(username=request.user)
    finally:
        cart.save()
        cartitem = None
        product = Product.objects.filter(reference=reference)[0]
        try:
            cartitem = CartItem.objects.filter(item=product)[0]
            cartitem.quantity += int(quantity)
        except ObjectDoesNotExist:
            cartitem = CartItem()
            cartitem.item = product
            cartitem.quantity = quantity
            cartitem.save()
            cart.cartitems.add(cartitem)
        finally:
            cartitem.save()
            cart.save()
        return redirect('/product/' + reference + '/')


def product(request, reference):
    debug = ""
    # reference = "'"+reference+"'"

    product = Product.objects.filter(reference__exact=reference)[:1]
    if not product:
        debug += str(product)
        return render(request, "product/notfound.html")

    if (product is None):
        if request.user.is_authenticated:
            return redirect("/dashboard/")
        else:
            return redirect("/")
    else:

        data = {}
        data["debug"] = str(debug)
        data["product"] = product

        images = Product_Image.objects.filter(reference=product)
        data["images"] = images
        return render(request, 'product/product.html', data)
    return render(request, "store/store.html")


def addproduct(request):

    return render(request, 'main/add_product.html')


@login_required()
def checkout(request):
    context = {}

    return render(request, 'store/checkout.html', context)


def data_add_product(request):
    data = {}
    input = request.POST
    pro = Product()
    pro.category_id = int(input["category"])
    pro.city_id = int(input["ville"])
    pro.name = input["title"]
    pro.owner = Person.objects.get(pk=request.user.id)
    pro.price = float(input["Prix"])
    pro.TS = bool(int(input['type_TRA']))
    pro.save()
    i = input.keys()
    for key in i:
        if key == 'image0':
            pr_img = Product_Image()
            pr_img.reference = pro
            pr_img.image_base64 = input[key]
            pr_img.save()
    data["added"] = True
    
    return redirect('index')
