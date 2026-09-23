from django.core.validators import MinLengthValidator
from django.db import models

from photos.validator import FileSizeValidator


class Photo(models.Model):
    photo = models.ImageField(
        validators=[
            FileSizeValidator(5),
        ]
    )
    description = models.CharField(
        max_length=100,
        validators=[
            MinLengthValidator(10),
        ],
        blank=True,
        null=True,
    )
    location = models.CharField(
        max_length=30,
    )
    tagged_pets = models.ManyToManyField(
        to='pets.Pet',
    )
    date_of_publication = models.DateField(
        auto_now=True,
    )
