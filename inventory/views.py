from datetime import date, timedelta

from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import FoodItemForm, SignUpForm
from .models import FoodItem

@login_required
def dashboard(request):
    """
    Main dashboard page.
    Shows all food items and highlights expiring / expired items.
    """
    today = date.today()

    # AUTO-EXPIRE LOGIC (Python advancement)
    FoodItem.objects.filter(
        user=request.user,
        expiry_date__lt=today
    ).exclude(status="EXPIRED").update(status="EXPIRED")

    # All items for the logged-in user
    items = FoodItem.objects.filter(user=request.user).order_by("expiry_date")

    # Items expiring in next 3 days
    expiring_soon = items.filter(
        expiry_date__gte=today,
        expiry_date__lte=today + timedelta(days=3),
        status__in=["FRESH", "EXPIRING", "DONATION_CANCELLED"],
    )

    # Already expired items (status-based ✔)
    expired = items.filter(status="EXPIRED")

    context = {
        "items": items,
        "expiring_soon": expiring_soon,
        "expired": expired,
        "today": today,
    }
    return render(request, "dashboard.html", context)


@login_required
def add_food_item(request):
    """
    Add a new food item.
    """
    if request.method == "POST":
        form = FoodItemForm(request.POST)
        if form.is_valid():
            food_item = form.save(commit=False)
            food_item.user = request.user
            food_item.save()
            messages.success(request, "Food item added successfully.")
            return redirect("dashboard")
    else:
        form = FoodItemForm()

    return render(request, "add_food_item.html", {"form": form})


@login_required
def edit_food(request, pk):
    """
    Edit an existing food item.
    """
    item = get_object_or_404(FoodItem, pk=pk, user=request.user)

    if request.method == "POST":
        form = FoodItemForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            messages.success(request, "Food item updated.")
            return redirect("dashboard")
    else:
        form = FoodItemForm(instance=item)

    return render(request, "edit_food.html", {"form": form, "item": item})


@login_required
def delete_food(request, pk):
    """
    Delete a food item after confirmation.
    """
    item = get_object_or_404(FoodItem, pk=pk, user=request.user)

    if request.method == "POST":
        item.delete()
        messages.success(request, "Food item deleted.")
        return redirect("dashboard")

    return render(request, "confirm_delete.html", {"item": item})


@login_required
def mark_as_donated(request, pk):
    """
    Mark a food item as donated.
    """
    item = get_object_or_404(FoodItem, pk=pk, user=request.user)

    if item.status in ["FRESH", "EXPIRING", "DONATION_CANCELLED"]:
        item.status = "DONATED"
        item.save()
        messages.success(request, f"{item.name} marked for donation.")
    else:
        messages.warning(request, "This item cannot be donated.")

    return redirect("dashboard")


@login_required
def cancel_donation(request, pk):
    """
    Cancel an already donated food item.
    """
    item = get_object_or_404(FoodItem, pk=pk, user=request.user)

    if item.status == "DONATED":
        item.status = "DONATION_CANCELLED"
        item.save()
        messages.info(request, f"Donation cancelled for {item.name}.")
    else:
        messages.warning(request, "This item is not marked for donation.")

    return redirect("dashboard")


@login_required
def mark_as_consumed(request, pk):
    """
    Mark a food item as consumed.
    """
    item = get_object_or_404(FoodItem, pk=pk, user=request.user)

    if item.status != "CONSUMED":
        item.status = "CONSUMED"
        item.save()
        messages.success(request, f"{item.name} marked as consumed.")

    return redirect("dashboard")


def signup(request):
    """
    User registration.
    """
    if request.user.is_authenticated:
        return redirect("dashboard")

    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Account created successfully. Welcome!")
            return redirect("dashboard")
    else:
        form = SignUpForm()

    return render(request, "registration/signup.html", {"form": form})

@login_required
def donation_history(request):
    """
    Shows all donated and donation-cancelled items for the user.
    """
    donated_items = FoodItem.objects.filter(
        user=request.user,
        status__in=["DONATED", "DONATION_CANCELLED"]
    ).order_by("-added_date")

    context = {
        "donated_items": donated_items
    }

    return render(request, "donation_history.html", context)
