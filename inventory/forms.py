from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import FoodItem

class FoodItemForm(forms.ModelForm):
    """
    Form used for adding and editing food items.
    """
    class Meta:
        model = FoodItem
        fields = ["name", "quantity", "category", "expiry_date", "notes"]

        widgets = {
            "expiry_date": forms.DateInput(attrs={"type": "date"}),
            "notes": forms.Textarea(attrs={"rows": 3}),
        }

        labels = {
            "name": "Food name",
            "quantity": "Quantity",
            "category": "Category (optional)",
            "expiry_date": "Expiry date",
            "notes": "Notes (optional)",
        }

class SignUpForm(UserCreationForm):
    """
    Simple signup form using Django's built-in User model.
    Adds an email field along with username and password.
    """

    email = forms.EmailField(required=True, help_text="Required. Enter a valid email address.")

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")
