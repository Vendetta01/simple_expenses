from django.contrib import admin

from .models import Account, Category, DataSource, Transaction
from .views import batch_update_view


class AccountAdmin(admin.ModelAdmin):
    list_display = ["name", "iban", "bic", "data_source"]
    list_filter = ["data_source"]
    search_fields = ["name", "iban"]


class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "parent"]
    list_filter = ["parent"]
    search_fields = ["name"]


class DataSourceAdmin(admin.ModelAdmin):
    list_display = ["name", "type", "source", "extract_timestamp"]
    list_filter = ["type"]
    search_fields = ["name", "source"]


class TransactionAdmin(admin.ModelAdmin):
    list_display = ["booking_date", "purpose", "category", "src", "dst", "amount", "type"]
    list_filter = ["booking_date", "category", "dst", "type"]
    search_fields = ["purpose", "dst"]
    actions = [
        "batch_update_category",
    ]

    @admin.action(description="Set category")
    def batch_update_category(self, request, queryset):
        return batch_update_view(
            model_admin=self,
            request=request,
            queryset=queryset,
            # this is the name of the field on the YourModel model
            field_name="category",
        )


admin.site.register(Account, AccountAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(DataSource, DataSourceAdmin)
admin.site.register(Transaction, TransactionAdmin)
