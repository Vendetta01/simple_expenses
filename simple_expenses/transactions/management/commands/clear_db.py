import argparse

from django.core.management.base import BaseCommand
from django.db import connection

from transactions.models import Account, Category, DataSource, Transaction


class Command(BaseCommand):
    help = "Drop all data from database"

    def add_arguments(self, parser):
        parser.add_argument("--dry-run", action=argparse.BooleanOptionalAction, default=True)
        parser.add_argument("--drop", action=argparse.BooleanOptionalAction, default=False)

    def handle(self, *args, **options):
        if options["dry_run"]:
            self.stdout.write("Dry run, so simply exiting...")
        else:
            if not options["drop"]:
                self.stdout.write("This is NOT a dry run, deleting all records now...")
                Transaction.objects.all().delete()
                Account.objects.all().delete()
                DataSource.objects.all().delete()
                Category.objects.all().delete()
            else:
                raise Exception("Not implemented yet")
                self.stdout.write("This is NOT a dry run, dropping all tables now...")
                # with connection.cursor() as cursor:
                #     cursor.execute("DROP TABLE transactions_transaction")
                #     cursor.execute("DROP TABLE transactions_transaction")
