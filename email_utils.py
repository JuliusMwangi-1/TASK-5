def send_order_email(email: str, order, items):
    print("=" * 50)
    print(f"Sending order confirmation to: {email}")
    print("ORDER SUMMARY")

    for item in items:
        print(
            f"Product ID: {item.product_id} | "
            f"Quantity: {item.quantity} | "
            f"Subtotal: {item.subtotal}"
        )

    print(f"Total Cost: {order.total_cost}")
    print("=" * 50)


def send_order_status_email(
    email: str,
    order_id: int,
    status: str
):
    print("=" * 50)
    print(f"Sending order status update to: {email}")
    print(f"Order ID: {order_id}")
    print(f"New Status: {status}")
    print("=" * 50)