from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Order, OrderItem


SHIPPING = 30


def get_order(request):
    order_id = request.session.get("order_id")

    if not order_id:
        order = Order.objects.create()
        request.session["order_id"] = order.id
        return order

    return Order.objects.get(id=order_id)


def home(request):
    products = Product.objects.all()[:4]
    return render(request, "home.html", {"products": products})


def shop(request):
    products = Product.objects.all()
    return render(request, "shop.html", {"products": products})


def cart(request):
    order = get_order(request)
    items = OrderItem.objects.filter(order=order)

    subtotal = sum(i.total() for i in items)
    total = subtotal + SHIPPING

    return render(request, "cart.html", {
        "items": items,
        "subtotal": subtotal,
        "shipping": SHIPPING,
        "total": total
    })

def product_detail(request, id):
    product = Product.objects.get(id=id)
    return render(request, 'product_detail.html', {
        'product': product
    })

def add_to_cart(request, id):
    product = get_object_or_404(Product, id=id)
    order = get_order(request)

    item, created = OrderItem.objects.get_or_create(
        order=order,
        product=product
    )

    if not created:
        item.quantity += 1
        item.save()

    return redirect("cart")


def increase_quantity(request, item_id):
    item = get_object_or_404(OrderItem, id=item_id)
    item.quantity += 1
    item.save()
    return redirect("cart")


def decrease_quantity(request, item_id):
    item = get_object_or_404(OrderItem, id=item_id)

    if item.quantity > 1:
        item.quantity -= 1
        item.save()
    else:
        item.delete()

    return redirect("cart")


def remove_item(request, item_id):
    item = get_object_or_404(OrderItem, id=item_id)
    item.delete()
    return redirect("cart")


def order(request):
    order = get_order(request)
    items = OrderItem.objects.filter(order=order)

    subtotal = sum(i.total() for i in items)
    shipping = SHIPPING
    total = subtotal + shipping

    return render(request, "order.html", {
        "items": items,
        "subtotal": subtotal,
        "shipping": shipping,
        "total": total
    })