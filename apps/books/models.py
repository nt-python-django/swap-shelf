from django.db import models
from apps.users.models import User


class BookCondition(models.TextChoices):
    NEW = "new", "New"
    GOOD = "good", "Good"
    FAIR = "fair", "Fair"
    WORN = "worn", "Worn"


class BookType(models.TextChoices):
    BORROW = "borrow", "Borrow"
    PERMANENT = "permanent", "Permanent"
    BOTH = "both", "Both"


class BookStatus(models.TextChoices):
    AVAILABLE = "available", "Available"
    UNAVAILABLE = "unavailable", "Unavailable"


class Genre(models.Model):
    name = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return self.name


class Book(models.Model):
    owner = models.ForeignKey(User, related_name="books", on_delete=models.CASCADE)
    title = models.CharField(max_length=124)
    author = models.CharField(max_length=64)
    genre = models.ForeignKey(Genre, related_name="books", on_delete=models.PROTECT)
    condition = models.CharField(
        choices=BookCondition.choices, default=BookCondition.GOOD
    )
    type = models.CharField(choices=BookType.choices, default=BookType.BORROW)
    description = models.CharField(max_length=999, blank=False)
    image = models.URLField()
    status = models.CharField(choices=BookStatus.choices, default=BookStatus.AVAILABLE)
    share = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
