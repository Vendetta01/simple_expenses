import argparse

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from transactions.load_data.helpers import read_files_into_dict
from transactions.load_data import categories, norisbank, vblh


class Command(BaseCommand):
    help = "Import data from csv"

    def add_arguments(self, parser):
        parser.add_argument("file_path", nargs="?", type=str)
        parser.add_argument("--skip-lines", type=int, default=0)
        parser.add_argument("--header", action=argparse.BooleanOptionalAction, default=True)
        parser.add_argument("--encoding", type=str, default="utf-8")
        parser.add_argument(
            "--source",
            type=str,
            choices=["categories", "category_mappings", "norisbank", "vblh"],
            default="norisbank",
        )

    def handle(self, *args, **options):
        # wrap whole import into single transaction so
        # import either succeeds or fails completely
        with transaction.atomic():
            # 1.) read files from path
            for _dict in read_files_into_dict(
                path=options["file_path"],
                skip_lines=options["skip_lines"],
                encoding=options["encoding"],
            ):
                if options["source"] == "norisbank":
                    norisbank.parse_dict_into_model(_dict=_dict)
                elif options["source"] == "vblh":
                    raise Exception("Not implemented yet")
                elif options["source"] == "categories":
                    categories.parse_dict_into_model(_dict=_dict)
                elif options["source"] == "category_mappings":
                    # read json and update all transactions
                    raise Exception("Not implemented yet")

                else:
                    raise CommandError(
                        (
                            f"Invalid value for source={options['source']}, "
                            "please choose one of {norisbank, vblh}"
                        )
                    )
