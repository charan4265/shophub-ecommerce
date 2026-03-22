# payments/views.py
# ─────────────────────────────────────────────
# Cash on Delivery payment flow
# ─────────────────────────────────────────────

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from orders.models import Order


@login_required
def payment_page(request, order_number):
    """
    Payment options page — shows COD and (future) online payment
    """
    order = get_object_or_404(
        Order, order_number=order_number, buyer=request.user
    )

    if order.payment_status == Order.PaymentStatus.PAID:
        messages.info(request, 'This order is already paid.')
        return redirect('orders:order_detail', order_number=order_number)

    return render(request, 'payments/payment_page.html', {'order': order})


@login_required
def confirm_cod(request, order_number):
    """
    Buyer confirms Cash on Delivery.
    Marks order as COD confirmed and status as Processing.
    """
    order = get_object_or_404(
        Order, order_number=order_number, buyer=request.user
    )

    if request.method == 'POST':
        order.payment_status = Order.PaymentStatus.COD
        order.status         = Order.Status.CONFIRMED
        order.save()
        messages.success(
            request,
            f'Order #{order.order_number} confirmed! Pay ₹{order.total_amount} on delivery.'
        )
        return redirect('payments:success', order_number=order_number)

    return redirect('payments:payment_page', order_number=order_number)


@login_required
def payment_success(request, order_number):
    """
    Order confirmed success page
    """
    order = get_object_or_404(
        Order, order_number=order_number, buyer=request.user
    )
    return render(request, 'payments/payment_success.html', {'order': order})