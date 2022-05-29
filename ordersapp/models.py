from django.db import models
from django.conf import settings
from mainapp.models import Accommodation


# Заказ
class Order(models.Model):
    FORMING = 'FM'
    SENT_TO_PROCEED = 'STP'
    PROCEEDED = 'PRD'
    PAID = 'PD'
    READY = 'RDY'
    CANCEL = 'CNL'

    ORDER_STATUS_CHOICES = (
        (FORMING, 'формируется'),
        (SENT_TO_PROCEED, 'отправлен в обработку'),
        (PROCEEDED, 'оплачен'),
        (PAID, 'обрабатывается'),
        (READY, 'подтверждён размещением'),
        (CANCEL, 'отменён'),
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created = models.DateTimeField(verbose_name='создан', auto_now_add=True)
    updated = models.DateTimeField(verbose_name='обновлён', auto_now=True)
    status = models.CharField(verbose_name='статус', max_length=3, choices=ORDER_STATUS_CHOICES, default=FORMING)
    is_active = models.BooleanField(verbose_name='активен', default=True)

    class Meta:
        ordering = ('-created',)
        verbose_name = 'заказ'
        verbose_name_plural = 'заказы'

    def __str__(self):
        return f'Текущий заказ: {self.id} '

    def get_total_nights(self):
        accommodations = self.orderitems.select_related()
        return sum(list(map(lambda x: x.nights, accommodations)))

    def get_total_cost(self):
        accommodation = self.orderitems.select_related()
        return sum(list(map(lambda x: x.nights * x.accommodation.price,
                            accommodation)))

    def delete(self):
        for item in self.orderitems.select_related():
            item.accommodation.availability += item.nights
            item.accommodation.save()

        self.is_active = False
        self.save()


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='orderitems', on_delete=models.CASCADE)
    accommodation = models.ForeignKey(Accommodation, verbose_name='размещение', on_delete=models.CASCADE)
    nights = models.PositiveIntegerField(verbose_name='количество', default=0)

    def get_accommodation_cost(self):
        return self.accommodation.price * self.nights
