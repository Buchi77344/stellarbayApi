

# Register your models here.
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, APIEndpoint, APIRequestLog, DashboardStats


# ✅ Custom User Admin
@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ("username", "email", "first_name", "last_name", "is_staff", "is_active")
    search_fields = ("username", "email")
    ordering = ("username",)


# ✅ APIEndpoint Admin
@admin.register(APIEndpoint)
class APIEndpointAdmin(admin.ModelAdmin):
    list_display = ("name", "method", "url", "is_active", "created_by", "created_at")
    list_filter = ("method", "is_active", "created_at")
    search_fields = ("name", "url", "description")
    autocomplete_fields = ("created_by",)
    ordering = ("-created_at",)


# ✅ APIRequestLog Admin
@admin.register(APIRequestLog)
class APIRequestLogAdmin(admin.ModelAdmin):
    list_display = ("method", "url", "status_code", "response_time", "user", "created_at")
    list_filter = ("status_code", "method", "created_at")
    search_fields = ("url", "method")
    autocomplete_fields = ("user", "endpoint")
    ordering = ("-created_at",)


# ✅ DashboardStats Admin
@admin.register(DashboardStats)
class DashboardStatsAdmin(admin.ModelAdmin):
    list_display = ("total_endpoints", "total_requests", "success_rate", "avg_response_time", "calculated_at")
    ordering = ("-calculated_at",)
