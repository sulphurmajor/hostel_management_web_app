from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from hostel.forms import (
    HostelForm,
    PaymentForm,
    RoomForm,
    StudentForm,
    VisitorForm,
    WardenForm,
)
from hostel.models import Hostel, Payments, Student, Visitor, Warden, room


ENTITIES = {
    "students": {
        "title": "Students",
        "model": Student,
        "form": StudentForm,
        "columns": [
            ("First name", "first_name"),
            ("Last name", "last_name"),
            ("Email", "email"),
            ("Birth date", "birth_date"),
            ("Courses", "no_of_courses"),
            ("Gender", "gender"),
            ("Hostel", "hostel"),
        ],
    },
    "hostels": {
        "title": "Hostels",
        "model": Hostel,
        "form": HostelForm,
        "columns": [
            ("Name", "name"),
            ("Address", "address"),
            ("Total rooms", "total_rooms"),
            ("Location", "location"),
        ],
    },
    "wardens": {
        "title": "Wardens",
        "model": Warden,
        "form": WardenForm,
        "columns": [
            ("First name", "first_name"),
            ("Last name", "last_name"),
            ("Email", "email"),
            ("Gender", "gender"),
            ("Hostel", "hostel"),
        ],
    },
    "rooms": {
        "title": "Rooms",
        "model": room,
        "form": RoomForm,
        "columns": [
            ("Room number", "room_number"),
            ("Capacity", "capacity"),
            ("Hostel", "hostel"),
            ("Status", "status"),
        ],
    },
    "payments": {
        "title": "Payments",
        "model": Payments,
        "form": PaymentForm,
        "columns": [
            ("Student", "student"),
            ("Amount", "amount"),
            ("Paid", "make_payment"),
            ("Date", "date"),
            ("Reason", "reason"),
        ],
    },
    "visitors": {
        "title": "Visitors",
        "model": Visitor,
        "form": VisitorForm,
        "columns": [
            ("Visitor", "visitor_name"),
            ("Phone", "phone_number"),
            ("Student visited", "student"),
            ("Purpose", "purpose"),
            ("Visit date", "visit_date"),
        ],
    },
}


def _entity_config(entity):
    try:
        return ENTITIES[entity]
    except KeyError as exc:
        raise Http404("Management page not found.") from exc


def _management_context(entity, config, form, success_message=""):
    columns = config["columns"]
    records = []
    for item in config["model"].objects.all():
        cells = []
        for label, field_name in columns:
            display_method = getattr(item, f"get_{field_name}_display", None)
            value = display_method() if display_method else getattr(item, field_name)
            cells.append(value if value not in (None, "") else "—")
        records.append(
            {
                "cells": cells,
                "edit_url": reverse("entity_edit", args=(entity, item.pk)),
                "delete_url": reverse("entity_delete", args=(entity, item.pk)),
            }
        )

    return {
        "entity": entity,
        "title": config["title"],
        "form": form,
        "columns": [label for label, _ in columns],
        "records": records,
        "success_message": success_message,
    }


def index_view(request):
    return render(request, "index.html")


@login_required
def entity_manage_view(request, entity):
    config = _entity_config(entity)
    form = config["form"](request.POST if request.method == "POST" else None)
    success_message = ""
    if request.method == "POST" and form.is_valid():
        form.save()
        success_message = f"{config['title'][:-1] if config['title'].endswith('s') else config['title']} added successfully."
        form = config["form"]()

    context = _management_context(entity, config, form, success_message)
    template = "visitor_form.html" if entity == "visitors" else "entity_manage.html"
    return render(request, template, context)


@login_required
def entity_edit_view(request, entity, item_id):
    config = _entity_config(entity)
    item = get_object_or_404(config["model"], pk=item_id)
    form = config["form"](request.POST or None, instance=item)
    success_message = ""
    if request.method == "POST" and form.is_valid():
        form.save()
        success_message = f"{config['title'][:-1] if config['title'].endswith('s') else config['title']} updated successfully."
        form = config["form"](instance=item)

    context = _management_context(entity, config, form, success_message)
    context["item"] = item
    return render(request, "entity_edit.html", context)


@login_required
def entity_delete_view(request, entity, item_id):
    config = _entity_config(entity)
    item = get_object_or_404(config["model"], pk=item_id)
    if request.method == "POST":
        item.delete()
        return redirect("entity_manage", entity=entity)

    return render(
        request,
        "entity_delete.html",
        {"entity": entity, "title": config["title"], "item": item},
    )


def student_form_view(request):
    return entity_manage_view(request, "students")


def hostel_form_view(request):
    return entity_manage_view(request, "hostels")


def warden_form_view(request):
    return entity_manage_view(request, "wardens")


def room_form_view(request):
    return entity_manage_view(request, "rooms")


def payments_view(request):
    return entity_manage_view(request, "payments")


def visitor_form_view(request):
    return entity_manage_view(request, "visitors")


def edit_student_view(request, student_id):
    return entity_edit_view(request, "students", student_id)


def delete_student_view(request, student_id):
    return entity_delete_view(request, "students", student_id)
