from .models import Product, ProductOrder, Order, Customer


class CustomerCart:
    """Корзина пользователя"""
    def __init__(self, request, product_slug=None, action=None):

        self.user = request.user
        if product_slug and action:
            """Метод будет срабатывать сразу, когда в CustomerCart будут переданы оба эти значения
            Нет необходимости вызывать этот метод через точку"""
            self.add_or_delete(product_slug, action)

    def get_product_cart(self):
        """Получаем данные, или если их нет, создаём новые"""
        customer, created = Customer.objects.get_or_create(user=self.user)

        order, created = Order.objects.get_or_create(customer=customer, payment=False)
        order_products = order.product_orders.all()

        order_total_price = order.get_order_total_price
        order_total_quantity = order.get_order_total_quantity

        return {
            'order_total_price': order_total_price,
            'order_total_quantity': order_total_quantity,
            'order': order,
            'order_products': order_products
        }

    def add_or_delete(self, product_slug, action):
        """Метод добавления или удаления товара в корзине"""
        order = self.get_product_cart()['order']  # Получаем заказ через метод
        product = Product.objects.get(slug=product_slug)
        order_product, created = ProductOrder.objects.get_or_create(order=order, product=product)

        if action == 'add' and product.quantity > 0 and product.quantity > order_product.quantity:
            """Добавим товар, если количество продукта на складе больше нуля и больше, чем заказал покупатель"""
            order_product.quantity += 1
        elif action == 'delete':
            order_product.quantity -= 1
        elif product_slug == 'delete_all' and action == 'delete_all':  # Очищаем всю корзину полностью
            order_product.quantity = 0

        order_product.save()

        if order_product.quantity <= 0:
            order_product.delete()

    def clear_cart(self):
        """Очищаем корзину и делаем заказ оплаченным"""
        order = self.get_product_cart()['order']
        order_products = self.get_product_cart()['order_products']

        for product in order_products:
            item = Product.objects.get(pk=product.product.pk)
            item.quantity -= product.quantity
            item.save()

        order.payment = True
        order.save()


def get_cart_data(request):
    """Вызываем класс CustomerCart и получаем данные корзины"""
    order = CustomerCart(request)
    order_info = order.get_product_cart()
    return order_info





