from transactions.models import Category


def parse_dict_into_model(
    _dict: dict,
) -> None:
    parent = None
    if _dict["parent"] and _dict["parent"] != "":
        parent = Category.objects.get(name=_dict["parent"])

    new_category = Category(name=_dict["name"], parent=parent)

    try:
        Category.objects.get(name=new_category.name)
    except Category.DoesNotExist:
        new_category.save()
    else:
        print(f"Skipping existing category {new_category=}")
