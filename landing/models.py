from django.db import models


# Create your models here.
class Subscriber(models.Model):
    email = models.EmailField(verbose_name='E-mail')
    name = models.CharField(verbose_name='Имя', max_length=128)
    is_active = models.BooleanField(verbose_name='Рассылка', default=True)

    class Meta:
        verbose_name = 'Подписчик'
        verbose_name_plural = 'Подписчики'

    def __str__(self):
        return "Рассылка для %s (%s)" % (self.email, self.name)
