from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404

from store.settings import STRIPE_SECRET_KEY
from .models import *
from django.views.generic import ListView, DetailView
from django.contrib.auth import login, logout
from .forms import LoginForm, RegistrationForm, EditProfileForm, EditUserForm, ShippingAddressForm
from .utils import CustomerCart, get_cart_data
import stripe


class ProductListView(ListView):
    """Вьюшка вывода категорий через модель Product"""
    model = Product
    context_object_name = 'categories'
    template_name = 'digital/index.html'
    extra_context = {'title': 'Магазин электроники Digital Store'}

    def get_queryset(self):
        categories = Category.objects.filter(parent__isnull=False)  # Фильтрация для вывода категорий с родителями
        return categories


class ProductDetailView(DetailView):
    """Вьюшка вывода деталей товара"""
    model = Product
    context_object_name = 'product'
    template_name = 'digital/product_detail.html'

    def get_context_data(self, **kwargs):
        """Получаем один и несколько товаров одной категории"""
        context = super().get_context_data()

        product = Product.objects.get(slug=self.kwargs['slug'])  # Один товар с описанием характеристик
        # Товары той же категории для списка рекомендаций на деталях товара
        products = Product.objects.filter(category=product.category).exclude(slug=product.slug)
        # Вытаскиваем ключ и значение характеристик в одном запросе
        spec_values = SpecValue.objects.filter(product=product).select_related('spec')

        context['title'] = product.title
        context['products'] = products
        context['spec_values'] = spec_values
        context['category'] = product.category

        return context


class ProductByCategoryView(ListView):
    """Вьюшка для отображения товаров по категориям, и их фильтрации"""
    model = Product
    context_object_name = 'products'
    template_name = 'digital/category_page.html'
    paginate_by = 3

    def get_queryset(self):
        """Получаем товары по категории и фильтруем по параметрам"""
        category = Category.objects.get(slug=self.kwargs['slug'])
        products = Product.objects.filter(category=category)

        # Фильтрация продуктов по ключам из запроса QuerySet (то, что пользователь будет отправлять через фильтрацию)
        model = self.request.GET.get('model')
        color_name = self.request.GET.get('color')
        price_from = self.request.GET.get('from')
        price_till = self.request.GET.get('till')

        # Получаем конкретные продукты из базы с помощью фильтрации
        if model:
            products = products.filter(model__title=model)
        if color_name:
            products = products.filter(color_name=color_name)
        if price_from:
            products = products.filter(price__gte=price_from)
            # [i for i in products if int(i.price) >= int(price_from)]
        if price_till:
            products = products.filter(price__lte=price_till)
            # [i for i in products if int(i.price) <= int(price_till)]
        return products

    def get_context_data(self, *, object_list=None, **kwargs):
        """Вытаскиваем модели и цвета конкретного товара"""
        context = super().get_context_data()

        category = Category.objects.get(slug=self.kwargs['slug'])
        products = Product.objects.filter(category=category)

        context['models'] = list(set(i.model for i in products))
        context['color_names'] = list(set([i.color_name for i in products]))
        context['prices'] = [i for i in range(200, 2000, 200)]

        context['query'] = self.request.GET
        context['title'] = category.title

        return context


class SearchView(ProductListView):
    """Вьюшка для поиска товаров"""
    def get_queryset(self):
        """Обработка поиска (то, что пользователь ввёл в строку поиска)"""
        word = self.request.GET.get('q')
        product = Product.objects.filter(title__icontains=word)

        return product

    def get_context_data(self, **kwargs):
        """Вытаскиваем данные по результату поиска"""
        # Можно убрать get_queryset и использовать только get_context data
        context = super().get_context_data(**kwargs)

        search_results = self.get_queryset()
        # Выводим на страницу категории в INDEX, но продукты получаем из PRODUCTS
        context['categories'] = [{'products': search_results}]

        return context


def login_view(request):
    """Вьюшка для логина пользователя"""
    if request.user.is_authenticated:
        return redirect('main')

    else:
        if request.method == 'POST':
            form = LoginForm(data=request.POST)
            if form.is_valid():
                user = form.get_user()
                if user:
                    login(request, user)
                    return redirect('main')

                else:
                    return redirect('login')
            else:
                return redirect('login')
        else:
            form = LoginForm()

        context = {
            'title': 'Авторизация пользователя',
            'login_form': form
        }

        return render(request, 'digital/login.html', context)


def logout_view(request):
    """Вьюшка для выхода из аккаунта"""
    if request.user.is_authenticated:
        logout(request)
        return redirect('main')

    else:
        return redirect('main')


def register_view(request):
    """Вьюшка для регистрации пользователя"""
    if request.user.is_authenticated:
        return redirect('main')

    else:
        if request.method == 'POST':
            user_form = RegistrationForm(data=request.POST)
            # Создаётся ещё и профиль, для заполнения номера телефона и аватарки пользователя
            profile_form = EditProfileForm(request.POST, request.FILES)
            if user_form.is_valid() and profile_form.is_valid():
                user = user_form.save()
                profile = profile_form.save(commit=False)  # Создаётся профиль в базе данных
                profile.user = user  # Профиль связывается с аккаунтом
                profile.save()
                return redirect('login')

        else:
            user_form = RegistrationForm()
            profile_form = EditProfileForm()

        context = {
            'title': 'Регистрация пользователя',
            'register_form': user_form,
            'profile_form': profile_form
        }

        return render(request, 'digital/registration.html', context)


def add_favorite_product(request, slug):
    """Вьюшка для добавления продуктов в избранное"""
    if not request.user.is_authenticated:
        return redirect('login')

    else:
        user = request.user
        product = get_object_or_404(Product, slug=slug)
        favorite_products = FavoriteProduct.objects.filter(user=user)
        if user:
            if product in [i.product for i in favorite_products]:
                """Удаление продукта из избранного, если он есть"""
                fav_product = FavoriteProduct.objects.get(product=product, user=user)
                fav_product.delete()

            else:
                """Добавление продукта в избранное, если его нет"""
                FavoriteProduct.objects.create(product=product, user=user)

        next_page = request.META.get('HTTP_REFERER', 'main')  # При нажатии на кнопку, оставляет нас на той же странице
        return redirect(next_page)


class FavoriteProductsView(LoginRequiredMixin, ListView):
    """Страница с избранными товарами"""
    model = FavoriteProduct
    context_object_name = 'favorites'
    template_name = 'digital/favorites.html'
    login_url = 'login'
    extra_context = {
        'title': 'Избранные продукты'
    }

    def get_queryset(self):
        """Получаем список всех избранных продуктов пользователя"""
        favorites = FavoriteProduct.objects.filter(user=self.request.user)
        favorites = [i.product for i in favorites]
        return favorites


def control_product_order(request, slug, action):
    """Вьюшка для добавления или удаления продукта в корзине"""
    if not request.user.is_authenticated:
        return redirect('login')

    else:
        user_cart = CustomerCart(request, slug, action)  # Делаем выбор между ADD или DELETE
        next_page = request.META.get('HTTP_REFERER', 'main')
        return redirect(next_page)


def my_cart_view(request):
    """Вьюшка для отображения страницы с корзиной пользователя"""
    if not request.user.is_authenticated:
        return redirect('login')

    else:
        order_info = get_cart_data(request)
        order_products = order_info['order_products']
        products = Product.objects.all()[::-1][:8]  # Вывод последних товаров магазина (для рекомендации)

        context = {
            'title': 'Моя корзина',
            'order': order_info['order'],
            'order_products': order_products,
            'products': products
        }

        return render(request, 'digital/my_cart.html', context)


def delete_cart(request):
    """Вьюшка для полной очистки корзины"""
    if not request.user.is_authenticated:
        return redirect('login')

    else:
        order_info = get_cart_data(request)
        order_products = order_info['order_products']
        for order_product in order_products:
            order_product.delete()
        return redirect('my_cart')


def profile_view(request):
    """Вьюшка для профиля пользователя"""
    if not request.user.is_authenticated:
        return redirect('login')

    else:
        user = request.user
        profile = Profile.objects.get(user=user)

    #  Проверка на то, есть ли у пользователя заказы (является ли он Customer)
    try:
        customer = Customer.objects.get(user=request.user)
        orders = Order.objects.filter(customer=customer, payment=True)  # Вывод оплаченных заказов
        ordered_products = ProductOrder.objects.filter(order__in=orders)

    except:
        customer = None
        orders = []
        ordered_products = []

    context = {
        'title': 'Мой аккаунт',
        'profile': profile,
        'ordered_products': ordered_products[::-1]
    }

    return render(request, 'digital/profile.html', context)


def edit_profile_view(request):
    """Вьюшка для отображения профиля"""
    if not request.user.is_authenticated:
        return redirect('login')

    else:
        if request.method == 'POST':
            form_type = request.POST.get('form_type')
            # Разделение логики на два условия, чтобы форма принимала конкретный POST запросpy 
            if form_type == 'user_form':

                user_form = EditUserForm(data=request.POST, instance=request.user)
                if user_form.is_valid():
                    user_form.save()
                    return redirect('profile', request.user.username)

            elif form_type == 'profile_form':
                profile_form = EditProfileForm(request.POST, request.FILES, instance=request.user.profile)
                if profile_form.is_valid():
                    profile_form.save()
                    return redirect('profile')

            else:
                return redirect('profile')

        else:
            user_form = EditUserForm(instance=request.user)
            profile_form = EditProfileForm(instance=request.user.profile)

        context = {
            'title': 'Мой профиль',
            'user_form': user_form,
            'profile_form': profile_form,
        }

        return render(request, 'digital/edit_profile.html', context)


def checkout_view(request):
    """Вьюшка с оплатой товара"""
    if not request.user.is_authenticated:
        return redirect('login')

    else:
        order_info = get_cart_data(request)
        if order_info['order_products']:
            regions = Region.objects.all()
            # cities получаем по related_name в модели Region
            dict_city = {i.pk: [[j.title, j.pk] for j in i.cities.all()] for i in regions}

            context = {
                'title': 'Оформление заказа',
                'order': order_info['order'],
                'order_products': order_info['order_products'],
                'form': ShippingAddressForm(),
                'dict_city': dict_city,
            }

            return render(request, 'digital/checkout.html', context)

        else:
            # Если продуктов в заказе нет, переход обратно на последнюю страницу
            next_page = request.META.get('HTTP_REFERER', 'main')
            return redirect(next_page)


def create_checkout_session(request):
    """Вьюшка для оплаты заказа"""
    if not request.user.is_authenticated:
        return redirect('login')

    else:
        stripe.api_key = STRIPE_SECRET_KEY
        if request.method == 'POST':
            order_info = get_cart_data(request)
            shipping_form = ShippingAddressForm(data=request.POST)
            ship_address = ShippingAddress.objects.all()

            if shipping_form.is_valid():
                shipping = shipping_form.save(commit=False)
                shipping.customer = Customer.objects.get(user=request.user)
                shipping.order = order_info['order']

                #  Сохраняем, адрес отличается
                if order_info['order'] not in [i.order for i in ship_address]:
                    shipping.save()

            else:
                return redirect('checkout')

            order_price = order_info['order_total_price']
            session = stripe.checkout.Session.create(
                line_items=[{
                    'price_data': {
                        'currency': 'usd',
                        'product_data': {'name': 'Электроника Digital Store'},
                        'unit_amount': int(order_price) * 100
                    },

                    'quantity': 1,
                }],

                mode='payment',
                success_url=request.build_absolute_uri(reverse('success_payment')),
                cancel_url=request.build_absolute_uri(reverse('checkout'))
            )

            return redirect(session.url)


def success_payment(request):
    """Страница с успешной оплатой (удаляет корзину и закрывает заказ)"""
    if not request.user.is_authenticated:
        return redirect('login')

    else:
        cart = CustomerCart(request)
        cart.clear_cart()

        context = {
            'title': 'Успешно'
        }

        return render(request, 'digital/success_payment.html', context)


