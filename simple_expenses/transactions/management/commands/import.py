import argparse

from django.core.management.base import BaseCommand, CommandError

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
        # 1.) read files from path
        for _dict in read_files_into_dict(
            path=options["file_path"],
            skip_lines=options["skip_lines"],
            encoding=options["encoding"],
        ):
            if options["source"] == "norisbank":
                norisbank.parse_dict_into_model(_dict=_dict)
            elif options["source"] == "vblh":
                pass
            elif options["source"] == "categories":
                categories.parse_dict_into_model(_dict=_dict)
            elif options["source"] == "category_mappings":
                # read json and update all transactions
                pass

            else:
                raise CommandError(
                    (
                        f"Invalid value for source={options['source']}, "
                        "please choose oe of {norisbank, vblh}"
                    )
                )
