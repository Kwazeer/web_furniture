from django import template
from digital.models import Category, Product, FavoriteProduct

register = template.Library()

@register.simple_tag()
def get_categories():
    """Функция отображения категорий на всех страницах"""
    return Category.objects.filter(parent__isnull=False)


@register.simple_tag()
def get_color(model, category, series):
    """Функция получения цвета для конкретного товара"""
    products = Product.objects.filter(model=model, category=category, series=series)

    filtered_colors = {}
    for product in products:
        filtered_colors[product.color_code] = product

    return filtered_colors.values()


@register.simple_tag(takes_context=True)
def query_params(context, **kwargs):
    """Функция для получения нескольких параметров запроса"""
    query = context['request'].GET.copy()

    for key, value in kwargs.items():
        query[key] = value

    return query.urlencode()  # Превращает словарь в строку запроса


@register.simple_tag()
def get_favorites(user):
    """Получаем список всех избранных"""
    # Используем loft_tags для того, чтобы избранные отображались на каждой карточке с товаром на всех страницах
    favorites = FavoriteProduct.objects.filter(user=user)
    favorites = [i.product for i in favorites]
    return favorites


@register.simple_tag()
def get_discount_price(price, discount):
    percent = (price * discount) / 100
    price = price - percent
    return price





