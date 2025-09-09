from django.contrib import admin
from django.urls import path
from dashboard.views import dashboard_page, budget_api

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/budget/", budget_api, name="budget_api"),  # JSON API
    path("", dashboard_page, name="dashboard"),          # Home -> dashboard
]
