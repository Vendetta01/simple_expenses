import json

from django.core.management.base import BaseCommand

from transactions.models import Transaction


class Command(BaseCommand):
    help = "Export category mappings to json"

    def add_arguments(self, parser):
        parser.add_argument("file_path", nargs="?", type=str)

    def handle(self, *args, **options):
        transaction_categories = {}
        for transaction in Transaction.objects.all():
            category_name = transaction.category.name if transaction.category else None
            transaction_categories[category_name] = (
                transaction_categories.get(category_name) or []
            ) + [transaction._content_hash]

        with open(options["file_path"], "w") as f:
            f.write(json.dumps(transaction_categories, indent=4))
