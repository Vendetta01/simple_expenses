from django.core.exceptions import ValidationError
from django.http import HttpResponseRedirect
from django.shortcuts import render


def batch_update_view(model_admin, request, queryset, field_name):
    def remove_fields(form):
        for field in list(form.base_fields.keys()):
            if not field == field_name:
                del form.base_fields[field]
        return form

    form_class = remove_fields(model_admin.get_form(request))

    if request.method == "POST":
        form = form_class()

        # the view is already called via POST from the django admin changelist
        # here we have to distinguish between just showing the intermediary view via post
        # and actually confirming the bulk edits
        # for this there is a hidden field 'form-post' in the html template
        if "form-post" in request.POST:
            form = form_class(request.POST)
            has_batch_errors = False

            form.full_clean()  # form.is_valid() will not work well because <WorkEntry: None>
            cleaned_field_data = form.cleaned_data[field_name]
            for item in queryset.all():
                try:
                    setattr(item, field_name, cleaned_field_data)
                    item.clean()
                except ValidationError as e:
                    form.add_error(None, e)
                    has_batch_errors = True

            if has_batch_errors:
                return render(
                    request,
                    "admin/work_entry_change_multiple_intermediate.html",
                    context={
                        "form": form,
                        "items": queryset,
                        "media": model_admin.media,
                    },
                )

            for item in queryset.all():
                setattr(item, field_name, cleaned_field_data)
                item.save()
            model_admin.message_user(
                request,
                "Changed field {} on {} items".format(
                    field_name,
                    queryset.count(),
                ),
            )
            return HttpResponseRedirect(request.get_full_path())

        return render(
            request,
            "admin/work_entry_change_multiple_intermediate.html",
            context={
                "form": form,
                "items": queryset,
                "media": model_admin.media,
            },
        )
