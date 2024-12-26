from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


class Category(models.Model):
    """Все категории"""
    title = models.CharField(max_length=100, verbose_name='Название')
    icon = models.ImageField(upload_to='icons/', null=True, blank=True, verbose_name='Иконка')
    slug = models.SlugField(unique=True, null=True, verbose_name='Слаг категории')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True,
                               verbose_name='Категория', related_name='subcategories')

    def get_absolute_url(self):
        return reverse('category', kwargs={'slug': self.slug})

    def get_icon(self):
        if self.icon:
            return self.icon.url
        else:
            return '😥'

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'категорию'
        verbose_name_plural = 'категории'


class Product(models.Model):
    """Детали телефона"""
    title = models.CharField(max_length=150, verbose_name='Название')
    price = models.IntegerField(default=0, verbose_name='Цена')
    quantity = models.IntegerField(default=0, verbose_name='Количество')
    color_name = models.CharField(max_length=30, verbose_name='Цвет')
    color_code = models.CharField(max_length=10, verbose_name='Код цвета')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата изменения')
    slug = models.SlugField(unique=True, null=True, verbose_name='Слаг продукта')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='products',
                                 verbose_name='Категория')
    model = models.ForeignKey('Model', on_delete=models.CASCADE, related_name='models', verbose_name='Модель')
    series = models.ForeignKey('Series', null=True, blank=True, on_delete=models.CASCADE, related_name='model_series',
                               verbose_name='Серия')
    discount = models.IntegerField(null=True, blank=True, verbose_name='Скидка')

    def get_absolute_url(self):
        return reverse('product', kwargs={'slug': self.slug})

    # Получаем images и first(), потому что обращаемся к related_name
    def get_photo(self):
        if self.images:
            return self.images.first().image.url
        else:
            return '-'

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'продукт'
        verbose_name_plural = 'продукты'


class ProductImage(models.Model):
    """Фотографии телефонов"""
    image = models.ImageField(upload_to='images/', null=True, blank=True, verbose_name='Фото продукта')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images', verbose_name='Продукт')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')

    def __str__(self):
        return self.product.title

    class Meta:
        verbose_name = 'фото'
        verbose_name_plural = 'фото'


class Model(models.Model):
    """Модель телефона"""
    title = models.CharField(max_length=150, verbose_name='Модель')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'модель'
        verbose_name_plural = 'модели'


class Spec(models.Model):
    """Модель характеристик КЛЮЧ"""
    title = models.CharField(max_length=100, verbose_name='Характеристика')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='spec_keys', verbose_name='Категория')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'характеристика'
        verbose_name_plural = 'характеристики'


class SpecValue(models.Model):
    """Модель характеристик ЗНАЧЕНИЕ"""
    value = models.CharField(max_length=200, verbose_name='Значение характеристики')
    spec = models.ForeignKey(Spec, on_delete=models.CASCADE, related_name='spec_values', verbose_name='Характеристика')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='products', verbose_name='Продукт')

    def __str__(self):
        return self.spec.title

    class Meta:
        verbose_name = 'значение характеристики'
        verbose_name_plural = 'значение характеристик'


class Series(models.Model):
    """Модель для серии модели продукта"""
    title = models.CharField(max_length=200, verbose_name='Название серии')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'серию'
        verbose_name_plural = 'серии'


class Profile(models.Model):
    """Модель профиля пользователя"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True, verbose_name='Фото')
    phone = models.CharField(max_length=30, null=True, blank=True, verbose_name='Телефон', default='Не указано')
    address = models.CharField(max_length=100, null=True, blank=True, verbose_name='Адрес (ул. дом. кв.)',
                               default='Не указано')
    region = models.CharField(max_length=50, null=True, blank=True, verbose_name='Регион', default='Не указано')
    city = models.CharField(max_length=50, null=True, blank=True, verbose_name='Город', default='Не указано')

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = 'профиль'
        verbose_name_plural = 'профили'


class FavoriteProduct(models.Model):
    """Модель избранных товаров пользователя"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Продукт')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')

    def __str__(self):
        return f'{self.user.username} : {self.product.title}'

    class Meta:
        verbose_name = 'избранный продукт'
        verbose_name_plural = 'избранные продукты'


class Customer(models.Model):
    """Модель пользователя для заказа"""
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, verbose_name='Пользователь')

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = 'покупатель'
        verbose_name_plural = 'покупатели'


class Order(models.Model):
    """Модель заказа"""
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, verbose_name='Покупатель')
    is_completed = models.BooleanField(default=False, verbose_name='Статус заказа')
    payment = models.BooleanField(default=False, verbose_name='Статус оплаты')  # Возможность оплаты
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата оформления заказа')
    shipping = models.BooleanField(default=True, verbose_name='Доставка')  # Возможность доставки

    def __str__(self):
        return f'{self.pk}: {self.customer.user.username}'

    class Meta:
        verbose_name = 'заказ'
        verbose_name_plural = 'заказы'

    @property
    def get_order_total_price(self):
        """Выводим все продукты в заказе"""
        order_products = self.product_orders.all()
        total_price = sum([i.get_total_price for i in order_products])
        return total_price

    @property
    def get_order_total_quantity(self):
        """Выводим количество продуктов в заказе"""
        order_products = self.product_orders.all()
        total_quantity = sum([i.quantity for i in order_products])
        return total_quantity


class ProductOrder(models.Model):
    """Модель товаров в заказе"""
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, verbose_name='Заказ',
                              related_name='product_orders')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, verbose_name='Продукт',
                                related_name='products_orders')
    quantity = models.IntegerField(default=0, verbose_name='Количество')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата изменения')

    def __str__(self):
        return f'Заказ {self.order.pk}: {self.product.title}'

    class Meta:
        verbose_name = 'заказанный продукт'
        verbose_name_plural = 'заказанные продукты'

    # Место для подсчёта скидки

    @property  # Использование метода вне этого класса, например в get_order_total_price
    def total_price(self):
        """Общая цена продуктов"""
        return self.product.price * self.quantity

    @property
    def get_total_price(self):
        """Получаем цену продуктов с учётом скидки"""
        if self.product.discount:
            discount_price = (self.product.price * self.product.discount) / 100
            self.product.price -= discount_price

        return self.product.price * self.quantity


class ShippingAddress(models.Model):
    """Модель доставки заказанного товара"""
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, verbose_name='Покупатель')
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, verbose_name='Заказ')
    address = models.CharField(max_length=150, verbose_name='Адрес доставки (ул. дом. кв.)')
    phone = models.CharField(max_length=30, verbose_name='Номер телефона')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    region = models.ForeignKey('Region', on_delete=models.SET_NULL, null=True, verbose_name='Регион')
    city = models.ForeignKey('City', on_delete=models.SET_NULL, null=True, verbose_name='Город')

    def __str__(self):
        return f'Покупатель: {self.customer.user.username}: {self.address}'

    class Meta:
        verbose_name = 'адрес доставки'
        verbose_name_plural = 'адреса доставки'


class Region(models.Model):
    """Модель региона доставки"""
    title = models.CharField(max_length=30, verbose_name='Регион')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'регион'
        verbose_name_plural = 'регионы'


class City(models.Model):
    """Модель города доставки"""
    title = models.CharField(max_length=20, verbose_name='Город')
    region = models.ForeignKey(Region, on_delete=models.SET_NULL, null=True, verbose_name='Регион', related_name='cities')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'город'
        verbose_name_plural = 'города'
