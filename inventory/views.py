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
    Main page for the user.
    Shows all items, plus items expiring soon and already expired.
    """
    today = date.today()
    # All items for this logged-in user
    items = FoodItem.objects.filter(user=request.user).order_by("expiry_date")
    # Items expiring in next 3 days
    expiring_soon = items.filter(
        expiry_date__lte=today + timedelta(days=3),
        expiry_date__gte=today,
        status__in=["FRESH", "EXPIRING"],
    )
    # Items already expired
    expired = items.filter(
        expiry_date__lt=today,
        status__in=["FRESH", "EXPIRING"],
    )

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
    item.status = "DONATED"
    item.save()
    messages.success(request, f"Marked {item.name} as donated.")
    return redirect("dashboard")

@login_required
def mark_as_consumed(request, pk):
    """
    Mark a food item as consumed.
    """
    item = get_object_or_404(FoodItem, pk=pk, user=request.user)
    item.status = "CONSUMED"
    item.save()
    messages.success(request, f"Marked {item.name} as consumed.")
    return redirect("dashboard")

def signup(request):
    """
    Allow a new user to register.
    After successful signup, the user is logged in and redirected to the dashboard.
    """
    # If already logged in, no need to sign up again
    if request.user.is_authenticated:
        return redirect("dashboard")

    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()          # creates the user
            login(request, user)        # log the user in immediately
            messages.success(request, "Account created successfully. Welcome!")
            return redirect("dashboard")
    else:
        form = SignUpForm()

    return render(request, "registration/signup.html", {"form": form})
