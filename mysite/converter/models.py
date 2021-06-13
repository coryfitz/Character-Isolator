from django.db import models

#This is supplying the options on the first page
class FilterPreference(models.Model):
    NONE = 'NO'
    first_250 = 'F250'
    first_500 = 'F500'
    first_750 = 'F750'
    first_1000 = 'F1000'
    PREFERENCE_CHOICES = [
        (NONE, 'None'),
        (first_250, 'First 250'),
        (first_500, 'First 500'),
        (first_750, 'First 750'),
        (first_1000, 'First 1000'),
    ]
    preference = models.CharField(
        max_length=100,
        choices=PREFERENCE_CHOICES,
        default=NONE,
    )

    def __str__(self):
        return self.preference

