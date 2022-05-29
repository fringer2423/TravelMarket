from django import template
from django.conf import settings

register = template.Library()


@register.filter(name='media_acc')
def media_acc(string):
    if not string:
        string = 'accommodation_img/default.jpg'

    return f'{settings.MEDIA_URL}{string}'


@register.filter(name='media_users')
def media_users(string):
    if not string:
        string = 'user_avatars/default.jpg'

    return f'{settings.MEDIA_URL}{string}'
