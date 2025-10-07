

# Register your models here.
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *


# ✅ Custom User admin
@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ("username", "email", "is_active", "is_staff", "is_seller", "is_buyer")
    list_filter = ("is_staff", "is_seller", "is_buyer", "is_active")
    search_fields = ("username", "email")
    ordering = ("id",)

    fieldsets = (
        (None, {"fields": ("username", "email", "password")}),
        ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        ("Roles", {"fields": ("is_seller", "is_buyer")}),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("username", "email", "password1", "password2", "is_seller", "is_buyer", "is_staff", "is_active"),
        }),
    )


# ✅ Profile admin
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "city", "country", "created_at")
    search_fields = ("user__username", "city", "country")
    list_filter = ("country", "created_at")


# ✅ Category admin
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    list_display = ("name", "slug", "created_at")
    search_fields = ("name",)
    ordering = ("name",)


# ✅ Product admin
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "price", "stock", "is_active", "seller", "created_at")
    list_filter = ("is_active", "category", "seller")
    search_fields = ("name", "description", "category__name")
    prepopulated_fields = {"slug": ("name",)}
    autocomplete_fields = ["category", "seller"]
    ordering = ("-created_at",)


# ✅ Inline for CartItem inside Cart
class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0


# ✅ Cart admin
@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ("user", "created_at", "total_price")
    search_fields = ("user__username", "user__email")
    inlines = [CartItemInline]
    readonly_fields = ("created_at",)


# ✅ OrderItem inline for Order
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ("product", "quantity", "price", "total_price")

    def total_price(self, obj):
        return obj.price * obj.quantity


# ✅ Order admin
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "status", "total_amount", "paid", "created_at")
    list_filter = ("status", "paid", "created_at")
    search_fields = ("user__username", "id", "payment_reference")
    readonly_fields = ("created_at", "updated_at", "total_amount")
    inlines = [OrderItemInline]
    ordering = ("-created_at",)


# ✅ Address admin
@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ("user", "full_name", "city", "country", "is_default")
    list_filter = ("country", "is_default")
    search_fields = ("user__username", "full_name", "city")


# ✅ Payment admin
@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ("order", "user", "amount", "payment_method", "status", "created_at")
    list_filter = ("payment_method", "status")
    search_fields = ("order__id", "user__username", "transaction_id")
    readonly_fields = ("created_at",)

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
