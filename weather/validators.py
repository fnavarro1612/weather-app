from django.core.exceptions import ValidationError

def validate_length(value):
    if len(value) < 5:
        raise ValidationError('Zip code must be 5 numbers long')
    return value