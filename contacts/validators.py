from django.core.validators import ValidationError
from django.utils.translation import gettext_lazy as _
def validate_phone_number(phone_number):
    for number in phone_number:
        if number is not('1234567890'):
            raise ValidationError(
                _('%(phone_number)s must have only digits'),
                params={'phone_number': phone_number},
                )
