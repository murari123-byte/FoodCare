from django.urls import path
from . import views

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("add/", views.add_food_item, name="add_food"),
    path("edit/<int:pk>/", views.edit_food, name="edit_food"),
    path("delete/<int:pk>/", views.delete_food, name="delete_food"),
    path("donated/<int:pk>/", views.mark_as_donated, name="mark_as_donated"),
    path("consumed/<int:pk>/", views.mark_as_consumed, name="mark_as_consumed"),
    path("donation-cancel/<int:pk>/", views.cancel_donation, name="cancel_donation"),
    path("donations/", views.donation_history, name="donation_history"),

    path("signup/", views.signup, name="signup"),
]
