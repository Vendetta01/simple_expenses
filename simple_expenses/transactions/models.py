from decimal import Decimal
from hashlib import sha256

import pendulum

from django.db import models


class BaseModel(models.Model):
    _content_hash = models.CharField(max_length=64, null=True, blank=True, editable=False)
    fields_to_hash = []

    @property
    def content_hash(self):
        content_str = ""
        for field in self.fields_to_hash:
            val = getattr(self, field)
            if isinstance(val, Decimal):
                content_str += str(val.normalize())
            else:
                content_str += str(val)

        return sha256(content_str.encode("utf-8")).hexdigest()

    def save(self, *args, **kwargs):
        # TODO: implement a more robust way to create and save the hash
        # Problem: type coersion only applies when writing to db, so
        # string representation may differ after writing to db...
        self._content_hash = self.content_hash
        super(BaseModel, self).save(*args, **kwargs)

    class Meta:
        abstract = True


class Category(BaseModel):
    name = models.CharField(max_length=255, null=False)
    parent = models.ForeignKey("self", null=True, on_delete=models.DO_NOTHING)

    load_timestamp = models.DateTimeField(default=pendulum.now)

    fields_to_hash = ["name", "parent"]

    def __str__(self):
        return self.name

    @classmethod
    def get_unmapped_pk(cls):
        # TODO: this is a dirty hack and should be refactored!
        try:
            return cls.objects.get(name="_unmapped").pk
        except:
            return None


class DataSource(BaseModel):
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=255)
    source = models.CharField(max_length=255, unique=True)
    extract_timestamp = models.DateTimeField()

    load_timestamp = models.DateTimeField(default=pendulum.now)

    fields_to_hash = ["name", "type", "source", "extract_timestamp"]

    def __str__(self):
        return self.name


class Account(BaseModel):
    name = models.CharField(max_length=255)
    iban = models.CharField(max_length=22, null=True, unique=True)
    bic = models.CharField(max_length=11, null=True)

    data_source = models.ForeignKey(DataSource, on_delete=models.DO_NOTHING)
    load_timestamp = models.DateTimeField(default=pendulum.now)

    fields_to_hash = ["name", "iban", "bic"]

    def __str__(self):
        return self.name


class Transaction(BaseModel):
    booking_date = models.DateField()
    settlement_date = models.DateField()
    amount = models.DecimalField(max_digits=22, decimal_places=4)
    currency = models.CharField(max_length=3)
    type = models.CharField(max_length=255, null=True)
    purpose = models.TextField()

    src = models.ForeignKey(
        Account, on_delete=models.DO_NOTHING, related_name="transaction_src_set"
    )
    dst = models.ForeignKey(
        Account, on_delete=models.DO_NOTHING, related_name="transaction_dst_set"
    )
    category = models.ForeignKey(
        Category, null=True, on_delete=models.DO_NOTHING, default=Category.get_unmapped_pk
    )
    data_source = models.ForeignKey(DataSource, on_delete=models.DO_NOTHING)
    load_timestamp = models.DateTimeField(default=pendulum.now)

    fields_to_hash = ["booking_date", "settlement_date", "amount", "currency", "type", "purpose"]

    def __str__(self):
        return f"{self.booking_date}: {self.purpose}"
