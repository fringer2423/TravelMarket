from collections import OrderedDict
from datetime import datetime
from urllib.parse import urlencode
from urllib.parse import urlunparse
from django.utils import timezone
from social_core.exceptions import AuthForbidden
import requests
from .models import TravelUserProfile


def save_user_profile(backend, user, response, *args, **kwargs):
    if backend.name != 'vk-oauth2':
        return

    api_url = urlunparse(('https',
                          'api.vk.com',
                          '/method/users.get',
                          None,
                          urlencode(OrderedDict(
                              fields=','.join(('bdate', 'sex', 'about')),
                              access_token=response['access_token'],
                              v='5.113')),
                          None
                          ))

    resp = requests.get(api_url)
    if resp.status_code != 200:
        return

    data = resp.json()['response'][0]
    if data['sex']:
        user.traveluserprofile.gender = TravelUserProfile.MALE if \
            data['sex'] == 2 else TravelUserProfile.FEMALE

    if data['about']:
        user.traveluserprofile.aboutMe = data['about']

    if data['bdate']:
        bdate = datetime.strptime(data['bdate'], '%d.%m.%Y').date()

        age = timezone.now().date().year - bdate.year
        if age < 18:
            user.delete()
            raise AuthForbidden('social_core.backends.vk.VKOAuth2')

    user.save()
