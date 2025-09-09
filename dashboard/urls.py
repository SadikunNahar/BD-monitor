from django.urls import path
from .views import dashboard_page, budget_api

urlpatterns = [
    path("", dashboard_page, name="dashboard"),
    path("api/budget/", budget_api, name="budget_api"),
]
