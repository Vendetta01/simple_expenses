import json

from django.db import transaction
from django.core.management.base import BaseCommand

from transactions.models import Category, Transaction


class Command(BaseCommand):
    help = "Import category mappings from json"

    def add_arguments(self, parser):
        parser.add_argument("file_path", nargs="?", type=str)

    def handle(self, *args, **options):
        with open(options["file_path"]) as f:
            category_mappings = json.loads(f.read())

        # TODO: this is totally inefficient but the simplest way to do it
        # Refactor into bulk_update (if possible) and remove direct model
        # dependency

        # category_name: [hash1, hash2, ...]
        with transaction.atomic():
            for category_name, content_hashes in category_mappings.items():
                category = Category.objects.get(name=category_name)
                for content_hash in content_hashes:
                    Transaction.objects.filter(_content_hash=content_hash).update(
                        category=category
                    )
