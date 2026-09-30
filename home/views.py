from django.shortcuts import render , get_object_or_404 , redirect
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import *
from django.core.paginator import Paginator

def index(request):
    trending_games = Game.objects.filter(is_trending=True)[:4]
    games = Game.objects.all()[:8]

    query = request.GET.get("q")
    category = request.GET.get("category")

    if query:
        games = games.filter(
            Q(title__icontains=query) |
            Q(category__icontains=query)
        )

    if category:
        games = games.filter(category=category)

    categories = Game.objects.values_list(
        "category",
        flat=True
    ).distinct()
    context = {
        "trending_games": trending_games,
        "games": games,
        "categories": categories,
        "selected_category": category,
    }
    return render(request, "index.html" , context)


def shop(request):

    query = request.GET.get("q")
    category = request.GET.get("category")
    sort = request.GET.get("sort" , "newest")

    games = Game.objects.all()

    if query:
        games = games.filter(
            Q(title__icontains=query) |
            Q(category__icontains=query)
        )

    if category:
        games = games.filter(category=category)

    sort_options = {
        "newest" : "-created_at" ,
        "oldest" : "created_at" ,
        "cheap" : "price" ,
        "expensive" : "-price" ,
    }
    games = games.order_by(sort_options.get(sort, "-created_at"))

    categories = Game.objects.values_list(
        "category",
        flat=True
    ).distinct()

    paginator = Paginator(games, 8)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "shop.html", {
        "games": page_obj,
        "query": query,
        "categories": categories,
        "selected_category": category,
        "selected_sort": sort,
    })


def contact(request):
    return render(request, "contact.html")


def product(request, id):

    game = get_object_or_404(Game, id=id)

    related_games = Game.objects.filter(
        category=game.category
    ).exclude(id=game.id)[:4]

    return render(request,"product_detail.html",{"game": game ,"related_games": related_games} )

@login_required(login_url="login")
def add_to_cart(request, game_id):

    if request.method != "POST":
        return redirect("shop")

    game = get_object_or_404(Game, id=game_id)

    cart, created = Cart.objects.get_or_create(
        user=request.user
    )

    quantity = int(request.POST.get("quantity", 1))

    item, created = CartItem.objects.get_or_create(
        cart=cart,
        game=game
    )

    if created:
        item.quantity = quantity
    else:
        item.quantity += quantity

    item.save()

    return redirect("cart")

@login_required(login_url="login")
def cart(request):

    cart, created = Cart.objects.get_or_create(
        user=request.user
    )

    return render(request, "cart.html", {"cart": cart})

def register(request):

    if request.method == "POST":

        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm = request.POST.get("confirm")

        if password != confirm:
            messages.error(request, "Password does not match")
            return redirect("register")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect("register")

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        Cart.objects.create(user=user)

        messages.success(request, "Account created successfully")

        return redirect("login")

    return render(request, "register.html")

def login_user(request):

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)
            return redirect("home")

        messages.error(request, "Username or Password is incorrect")

    return render(request, "login.html")

def logout_user(request):

    logout(request)

    return redirect("home")

@login_required(login_url="login")
def increase_quantity(request, item_id):

    item = get_object_or_404(
        CartItem,
        id=item_id,
        cart__user=request.user
    )

    item.quantity += 1
    item.save()

    return redirect("cart")

@login_required(login_url="login")
def decrease_quantity(request, item_id):

    item = get_object_or_404(
        CartItem,
        id=item_id,
        cart__user=request.user
    )

    if item.quantity > 1:
        item.quantity -= 1
        item.save()
    else:
        item.delete()

    return redirect("cart")

@login_required(login_url="login")
def remove_item(request, item_id):

    item = get_object_or_404(
        CartItem,
        id=item_id,
        cart__user=request.user
    )

    item.delete()

    return redirect("cart")

@login_required(login_url="login")
def checkout(request):

    cart, created = Cart.objects.get_or_create(
        user=request.user
    )

    return render(
        request,
        "checkout.html",
        {
            "cart": cart,
        }
    )

@login_required
def payment(request):
    cart = Cart.objects.get(user=request.user)
    if request.method == "POST":
        pass
    return render(request, "payment.html", {"cart": cart})