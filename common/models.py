from django.db import models


class Comment(models.Model):
    text = models.TextField(
        max_length=300
    )
    date_and_time_of_publication = models.DateTimeField(
        auto_now_add=True,
    )
    to_photo = models.ForeignKey(
        to='photos.Photo',
        on_delete=models.CASCADE,
    )


class Like(models.Model):
    to_photo = models.ForeignKey(
        to='photos.Photo',
        on_delete=models.CASCADE,
    )
