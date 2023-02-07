from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse

class GameCategory(models.Model):
    slug = models.SlugField()
    name = models.CharField(max_length=255)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('main:account_list_by_category', kwargs={'category_slug': self.slug})


# Аккаунты на продажу
class Product(models.Model):
    REGION_CHOICES = [
        ('EU', 'eu'),
        ('AP', 'ap'),
        ('NA', 'na'),
        ('OCEANIA', 'oceania')
    ]

    category = models.ForeignKey(GameCategory, related_name='category', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    slug = models.SlugField()
    # Полное описание на странице товара
    desc = models.TextField()
    # Наличие
    availability = models.IntegerField(default=1)
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    # Краткое описание товара на главной стр.
    overview = models.CharField(max_length=150)
    # Продавец
    salesman = models.ForeignKey(User, on_delete=models.CASCADE)
    region = models.CharField(max_length=20, choices=REGION_CHOICES, default='EU')

    class Meta:
        ordering = ('-created',)
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def __str__(self):
        return f"Продавец {self.salesman}, товар {self.title}"

    def get_absolute_url(self):
        return reverse('main:account_detail', kwargs={'product_pk': self.pk})



class Comments(models.Model):
    product = models.ForeignKey(Product, related_name='comm', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add=True)
    text = models.TextField()
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ('-created',)
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return f"Комментарий от пользователя {self.name}"


class ImageGallery(models.Model):
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    title = models.CharField(max_length=255, blank=True, default='new')
    image = models.ImageField(upload_to='pictures/image_gallery/%Y/%m/%d', blank=True, null=True)

    class Meta:
        verbose_name = 'Изображение для товаров'
        verbose_name_plural = 'Изображения для товаров'

    def __str__(self):
        return f'Изображение для {self.pk}'

class Orders(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    created = models.DateTimeField(auto_now_add=True)
    paid = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
        ordering = ('-created',)

    def __str__(self):
        return f"Заказ {self.id}"

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())


class OrderItem(models.Model):
    order = models.ForeignKey(Orders, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='order_items', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    availability = models.PositiveIntegerField(default=1)

    def get_cost(self):
        return self.price * self.availability

    def __str__(self):
        return str(self.pk)
