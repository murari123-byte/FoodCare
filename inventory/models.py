from datetime import date
from django.db import models
from django.contrib.auth.models import User

class FoodItem(models.Model):
    """
    A single food item owned by a user.
    We use this to track expiry and reduce wastage.
    """

    STATUS_CHOICES = [
        ("FRESH", "Fresh"),
        ("EXPIRING", "Expiring Soon"),
        ("EXPIRED", "Expired"),
        ("DONATE", "Marked for Donation"),
        ("DONATED", "Donated"),
        ("DONATION_CANCELLED", "Donation Cancelled"),
        ("CONSUMED", "Consumed"),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        help_text="The owner of this food item.",
    )

    name = models.CharField(
        max_length=100,
        help_text="Example: Milk, Rice, Apples",
    )

    quantity = models.CharField(
        max_length=50,
        help_text="Example: 1L, 2kg, 5 pieces",
    )

    category = models.CharField(
        max_length=50,
        blank=True,
        help_text="Optional: Fruits, Dairy, Grains, etc.",
    )

    added_date = models.DateField(
        auto_now_add=True,
        help_text="Automatically set when the item is created.",
    )

    expiry_date = models.DateField(
        help_text="When this item is expected to expire.",
    )

    status = models.CharField(
        max_length=30,
        choices=STATUS_CHOICES,
        default="FRESH",
    )

    notes = models.TextField(
        blank=True,
        help_text="Anything extra: brand, storage place, etc.",
    )

    def days_left(self) -> int:
        """
        Returns how many days are left until this item expires.
        Negative means it's already expired.
        """
        return (self.expiry_date - date.today()).days

    def __str__(self) -> str:
        # Helpful string when using Django admin or shell
        return f"{self.name} ({self.quantity})"
