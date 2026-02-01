from django import forms
from django.db import models
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    tel = forms.CharField(max_length=15, required=True)

    class Meta:
        model = User
        fields = ("username", "email", "tel", "password1", "password2")


class Images(models.Model):
    img = models.ImageField(upload_to='article', height_field=100, width_field=100)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    tel = models.CharField(max_length=15)


class Prescription(models.Model):
    STATUS_CHOICES = [
        ('active', 'Активный'),
        ('used', 'Использованный'),
        ('expired', 'Просроченный'),
        ('pending', 'На рассмотрении'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='prescriptions')
    doctor_name = models.CharField(max_length=200, verbose_name='ФИО врача')
    clinic = models.CharField(max_length=300, verbose_name='Лечебное учреждение')
    diagnosis = models.TextField(verbose_name='Диагноз', blank=True)
    date = models.DateField(auto_now_add=True, verbose_name='Дата выписки')
    expiry_date = models.DateField(verbose_name='Срок действия')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    notes = models.TextField(verbose_name='Примечания', blank=True)
    external_id = models.CharField(max_length=100, verbose_name='Номер рецепта (ID)', blank=True, null=True)
    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ['-date']

    def __str__(self):
        return f'Рецепт №{self.id} для {self.user.username}'

    def days_until_expiry(self):
        """Количество дней до истечения срока действия"""
        from datetime import date
        delta = self.expiry_date - date.today()
        return delta.days

    def is_expiring_soon(self):
        """Истекает ли рецепт скоро (менее 7 дней)"""
        return 0 <= self.days_until_expiry() <= 7


class Medicine(models.Model):
    FORM_CHOICES = [
        ('tablets', 'Таблетки'),
        ('capsules', 'Капсулы'),
        ('injection', 'Инъекции'),
        ('ointment', 'Мазь'),
        ('drops', 'Капли'),
        ('syrup', 'Сироп'),
        ('spray', 'Спрей'),
        ('powder', 'Порошок'),
    ]

    prescription = models.ForeignKey(Prescription, on_delete=models.CASCADE, related_name='medicines')
    name = models.CharField(max_length=200, verbose_name='Название препарата')
    dosage = models.CharField(max_length=100, verbose_name='Дозировка')
    form = models.CharField(max_length=50, choices=FORM_CHOICES, verbose_name='Форма выпуска')
    quantity = models.IntegerField(verbose_name='Количество')
    instructions = models.TextField(verbose_name='Инструкция по применению', blank=True)

    class Meta:
        verbose_name = 'Лекарство'
        verbose_name_plural = 'Лекарства'

    def __str__(self):
        return f'{self.name} {self.dosage}'


class Order(models.Model):
    STATUS_CHOICES = [
        ('processing', 'В обработке'),
        ('in_transit', 'В пути'),
        ('delivered', 'Доставлено'),
        ('cancelled', 'Отменено'),
        ('ready_for_pickup', 'Готов к выдаче'),
    ]

    prescription = models.ForeignKey(Prescription, on_delete=models.CASCADE, related_name='orders')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order_date = models.DateTimeField(auto_now_add=True)
    delivery_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='processing')
    pickup_point = models.CharField(max_length=300, verbose_name='Пункт выдачи')
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    discount = models.IntegerField(default=0, verbose_name='Скидка %')
    tracking_number = models.CharField(max_length=100, blank=True)
    notes = models.TextField(verbose_name='Примечания к заказу', blank=True)

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
        ordering = ['-order_date']

    def __str__(self):
        return f'Заказ №{self.id} для {self.user.username}'

    def final_price(self):
        """Итоговая цена с учетом скидки"""
        if self.price is None:
            return 0
        return self.price * (100 - self.discount) / 100

    def status_display(self):
        """Отображение статуса на русском"""
        status_map = {
            'processing': 'В обработке',
            'in_transit': 'В пути',
            'delivered': 'Доставлено',
            'cancelled': 'Отменено',
            'ready_for_pickup': 'Готов к выдаче',
        }
        return status_map.get(self.status, self.status)