from transactions.models import Category


def parse_dict_into_model(
    _dict: dict,
) -> None:
    parent = None
    if _dict["parent"] and _dict["parent"] != "":
        parent = Category.objects.get(name=_dict["parent"])
    Category.objects.create(name=_dict["name"], parent=parent)
