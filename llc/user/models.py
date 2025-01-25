from django.db import models
from django.utils import timezone

class Package(models.Model):
    tracking_number = models.CharField(max_length=255, unique=True, default="Not")  # Уникальный номер отслеживания
    when = models.DateTimeField(auto_now_add=True)  # Дата и время создания записи
    sender = models.CharField(max_length=255, default="Not")  # Имя отправителя
    recipient = models.CharField(max_length=255, default="Not")  # Имя получателя
    sender_adres = models.CharField(max_length=500, default="Not")  # Адрес отправителя
    recipient_adres = models.CharField(max_length=500, default="Not")  # Адрес получателя


    def __str__(self):
        return  [self.tracking_number, self.when, self.sender_adres, self.sender_adres, self.recipient_adres, self.recipient]