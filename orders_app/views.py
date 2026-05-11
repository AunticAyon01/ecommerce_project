from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Order
from .forms import OrderForm, OrderStatusForm
from products_app.models import Product


@login_required
def create_order(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    if not product.is_in_stock:
        messages.error(request, 'This product is out of stock.')
        return redirect('product_detail', pk=product_id)

    if request.method == 'POST':
        form = OrderForm(request.POST, product=product)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.product = product
            order.save()
            # Reduce stock
            product.stock -= order.quantity
            product.save()
            messages.success(request, f'Order placed successfully! Order #{order.pk}')
            return redirect('order_history')
    else:
        form = OrderForm(product=product)
    return render(request, 'orders_app/create_order.html', {'form': form, 'product': product})


@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, 'orders_app/order_history.html', {'orders': orders})


@login_required
def order_detail(request, pk):
    order = get_object_or_404(Order, pk=pk, user=request.user)
    return render(request, 'orders_app/order_detail.html', {'order': order})


@login_required
def cancel_order(request, pk):
    order = get_object_or_404(Order, pk=pk, user=request.user)
    if order.status in ['Pending', 'Processing']:
        if request.method == 'POST':
            order.status = 'Cancelled'
            order.save()
            # Restore stock
            order.product.stock += order.quantity
            order.product.save()
            messages.success(request, f'Order #{order.pk} cancelled.')
            return redirect('order_history')
        return render(request, 'orders_app/cancel_confirm.html', {'order': order})
    else:
        messages.error(request, 'This order cannot be cancelled.')
        return redirect('order_history')


@login_required
def all_orders(request):
    if not request.user.is_staff:
        messages.error(request, 'Access denied.')
        return redirect('home')
    orders = Order.objects.all()
    return render(request, 'orders_app/all_orders.html', {'orders': orders})
