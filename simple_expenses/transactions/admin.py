from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import Account, Category, DataSource, Transaction
from .views import batch_update_view


class BaseAdmin(admin.ModelAdmin):
    exclude = ("load_timestamp",)

    def get_actions(self, request):
        actions = super().get_actions(request)
        del actions["delete_selected"]

        return actions


class CategoryListFilter(admin.SimpleListFilter):
    title = _("Category")
    parameter_name = "category_id"

    def lookups(self, request, model_admin):
        # generate the list of choices
        categories = Category.objects.all()
        return [(category.pk, str(category)) for category in categories]

    def queryset(self, request, queryset):
        # filter the queryset by the selected value
        value = self.value()
        if value is not None:
            return queryset.filter(category_id=self.value())
        return queryset


class AccountAdmin(BaseAdmin):
    list_display = ["name", "iban", "bic", "data_source"]
    list_filter = ["data_source"]
    search_fields = ["name", "iban"]


class CategoryAdmin(BaseAdmin):
    list_display = ["name", "parent"]
    list_filter = ["parent__name"]
    search_fields = ["name"]


class DataSourceAdmin(BaseAdmin):
    list_display = ["name", "type", "source", "extract_timestamp"]
    list_filter = ["type"]
    search_fields = ["name", "source"]


class TransactionAdmin(BaseAdmin):
    list_display = ["booking_date", "purpose", "category", "src", "dst", "amount", "type"]
    list_filter = [
        "booking_date",
        CategoryListFilter,
        ("src", admin.RelatedOnlyFieldListFilter),
        "type",
    ]
    list_editable = ["category"]
    search_fields = ["purpose", "src__name"]
    actions = ["batch_update_category"]

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
