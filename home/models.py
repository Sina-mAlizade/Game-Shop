from django.db import models
from PIL import  Image
from django.contrib.auth.models import User


class Game(models.Model):
    CATEGORY_CHOICES = [
        ("Action", "Action"),
        ("Adventure", "Adventure"),
        ("Racing", "Racing"),
        ("Sport", "Sport"),
    ]


    title = models.CharField(max_length=200)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    image = models.ImageField(upload_to="games/")
    description = models.TextField()
    is_trending = models.BooleanField(default=False)
    is_most_played = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.image.path)

        img = img.resize((600, 600))

        img.save(self.image.path)


class Cart(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username

    @property
    def total_price(self):
        return sum(item.total_price() for item in self.items.all())

    @property
    def total_items(self):
        return sum(item.quantity for item in self.items.all())


class CartItem(models.Model):
    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        related_name="items"
    )

    game = models.ForeignKey(
        Game,
        on_delete=models.CASCADE
    )

    quantity = models.PositiveIntegerField(default=1)

    def total_price(self):
        return self.quantity * self.game.price


class Order(models.Model):

    STATUS_CHOICES = [
        ("Pending", "Pending"),
        ("Paid", "Paid"),
        ("Canceled", "Canceled"),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    full_name = models.CharField(max_length=200)

    phone = models.CharField(max_length=20)

    address = models.TextField()

    city = models.CharField(max_length=100)

    postal_code = models.CharField(max_length=20)

    total_price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="Pending"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id}"

class OrderItem(models.Model):

    order = models.ForeignKey(
        Order,
        related_name="items",
        on_delete=models.CASCADE
    )

    game = models.ForeignKey(
        Game,
        on_delete=models.CASCADE
    )

    quantity = models.PositiveIntegerField()

    price = models.DecimalField(
        max_digits=8,
        decimal_places=2
    )

    def total_price(self):
        return self.price * self.quantity