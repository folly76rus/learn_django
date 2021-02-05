from django.db import models


class Purchase(models.Model):
    payer_id = models.ForeignKey('Customer', on_delete=models.CASCADE)
    amount = models.FloatField('Сумма')
    persent = models.IntegerField('Процент')
    pay_date = models.DateTimeField('Дата покупки')

    def __str__(self):
        return str(self.amount)

    class Meta:
        verbose_name = 'Покупка'
        verbose_name_plural = 'Покупки'


class Customer(models.Model):
    first_name = models.CharField('Имя', max_length=50)
    last_name = models.CharField('Фамилия', max_length=50)
    country = models.CharField('Страна', max_length=50)

    def __str__(self):
        return self.last_name

    class Meta:
        verbose_name = 'Покупатель'
        verbose_name_plural = 'Покупатели'

