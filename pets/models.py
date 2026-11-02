from django.contrib.auth import get_user_model
from django.db import models
from django.utils.text import slugify


UserModel = get_user_model()


class Pet(models.Model):
    name = models.CharField(
        max_length=30,
    )
    personal_photo = models.URLField()
    date_of_birth = models.DateField(
        blank=True,
        null=True,
    )
    slug = models.SlugField(
        unique=True,
        blank=True,
        editable=False,
    )
    user = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
    )

    def __str__(self) -> str:
        return self.name

    def save(self, *args, **kwargs) -> None:
        super().save(*args, **kwargs)
        self.slug = slugify(f"{self.name}-{self.pk}")
        super().save(*args, **kwargs)
