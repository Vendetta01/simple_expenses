from datetime import datetime
from decimal import Decimal, Context

import pendulum

from transactions.models import Account, DataSource, Transaction


def parse_dict_into_model(
    _dict: dict,
) -> None:
    # skip for special case of last line containing current balance
    decimal_context = Context(prec=4)
    if _dict["Buchungstag"] == "Kontostand":
        pass
    else:
        purpose = _dict["Verwendungszweck"]
        type_ = _dict["Umsatzart"]
        booking_date = datetime.strptime(_dict["Buchungstag"], "%d.%m.%Y").date()
        try:
            settlement_date = datetime.strptime(_dict["Wert"], "%d.%m.%Y").date()
        except ValueError:
            settlement_date = booking_date

        amount = Decimal(
            (_dict["Soll"] or _dict["Haben"]).replace(".", "").replace(",", "."),
            context=decimal_context,
        ).normalize()
        currency = _dict["Währung"]

        if type_ == "Kartenzahlung":
            src_ = purpose.split("//")[0]
        else:
            src_ = _dict["Begünstigter / Auftraggeber"]

        data_source, created = DataSource.objects.get_or_create(
            source=_dict["file_url"],
            defaults={
                "name": _dict["file_url"],
                "type": "csv",
                "extract_timestamp": pendulum.now(),
            },
        )
        dst, created = Account.objects.get_or_create(
            name="norisbank_girokonto",
            defaults={
                "iban": "DE13100777770437267800",
                "bic": "NORSDE51XXX",
                "data_source": data_source,
            },
        )

        src, created = Account.objects.get_or_create(
            name=src_,
            defaults={
                "data_source": data_source,
            },
        )

        new_transaction = Transaction(
            booking_date=booking_date,
            settlement_date=settlement_date,
            amount=amount,
            purpose=purpose,
            type=type_,
            currency=currency,
            src=src,
            dst=dst,
            data_source=data_source,
        )

        try:
            Transaction.objects.get(_content_hash=new_transaction.content_hash)
        except Transaction.DoesNotExist:
            new_transaction.save()
        else:
            print(f"Skipping existing {new_transaction=}")
